from django.conf import settings
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, serializers, viewsets
from rest_framework.exceptions import ValidationError

from api.applications_api.serializers import ApplicationEventSerializer
from applications.models import (
    Application,
    ApplicationEventScheduleResult,
    Organisation,
    User, ApplicationEventSchedule,
)
from permissions.api_permissions import AllocationRequestPermission
from reservation_units.models import ReservationUnit
from django.utils.translation import gettext_lazy as _


class ScheduleResultScheduleSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=ApplicationEventSchedule.objects.all())
    declined_reservation_unit_ids = serializers.PrimaryKeyRelatedField(source="declined_reservation_units", queryset=ReservationUnit.objects.all(), many=True)
    class Meta:
        model = ApplicationEventSchedule
        fields = ["id", "declined_reservation_unit_ids"]

class ApplicationEventScheduleResultSerializer(serializers.ModelSerializer):
    applicant_id = serializers.PrimaryKeyRelatedField(
        source="application_event_schedule.application_event.application.user_id",
        read_only=True
    )
    applicant_name = serializers.SerializerMethodField()
    application_id = serializers.PrimaryKeyRelatedField(
        source="application_event_schedule.application_event.application_id",
        read_only=True
    )
    organisation_id = serializers.PrimaryKeyRelatedField(
        source="application_event_schedule.application_event.application.organisation_id",
        read_only=True
    )
    organisation_name = serializers.CharField(
        source="application_event_schedule.application_event.application.organisation.name", read_only=True
    )

    application_event = ApplicationEventSerializer(
        source="application_event_schedule.application_event", read_only=True
    )

    application_event_schedule = ScheduleResultScheduleSerializer()

    unit_name = serializers.SerializerMethodField()
    allocated_reservation_unit_name = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationEventScheduleResult
        fields = [
            "application_id",
            "applicant_id",
            "applicant_name",
            "organisation_id",
            "organisation_name",
            "unit_name",
            "allocated_reservation_unit_id",
            "allocated_reservation_unit_name",
            "application_event",
            "application_event_schedule",
            "allocated_duration",
            "allocated_day",
            "allocated_begin",
            "allocated_end",
        ]

    def update(self, instance, validated_data):
        schedule = validated_data.pop("application_event_schedule")
        if schedule["id"].id != instance.application_event_schedule.id:
            raise ValidationError(_("Application event schedule id is not updatable."))
        instance.application_event_schedule.declined_reservation_units.set(schedule["declined_reservation_units"])
        super().update(instance, validated_data)
        return instance

    def get_unit_name(self, instance):
        return instance.allocated_reservation_unit.unit.name

    def get_allocated_reservation_unit_name(self, instance):
        return instance.allocated_reservation_unit.name

    def get_applicant_name(self, instance):
        if instance.application_event_schedule.application_event.application.user:
            return (
                instance.application_event_schedule.application_event.application.user.get_full_name()
            )


class AllocationResultsFilter(filters.FilterSet):
    application_round_id = filters.NumberFilter(method="filter_application_round")
    applicant = filters.NumberFilter(method="filter_applicant")
    reservation_unit = filters.ModelChoiceFilter(
        field_name="allocated_reservation_unit", queryset=ReservationUnit.objects.all()
    )

    def filter_application_round(self, queryset, value, *args, **kwargs):
        round_id = args[0]
        return queryset.filter(
            application_event_schedule__application_event__application__application_round_id=round_id
        )

    def filter_applicant(self, queryset, value, *args, **kwargs):
        user_id = args[0]
        return queryset.filter(
            application_event_schedule__application_event__application__user_id=user_id
        )


class AllocationResultViewSet(viewsets.ModelViewSet):
    queryset = ApplicationEventScheduleResult.objects.all().order_by(
        "application_event_schedule__application_event_id"
    )
    serializer_class = ApplicationEventScheduleResultSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AllocationResultsFilter
    http_method_names = ['get', 'put', 'patch', 'head']
    permission_classes = (
        [AllocationRequestPermission]
        if not settings.TMP_PERMISSIONS_DISABLED
        else [permissions.AllowAny]
    )
