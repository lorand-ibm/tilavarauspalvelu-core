import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_permissions.mixins import AuthFilter, AuthNode
from graphene_permissions.permissions import AllowAuthenticated

from reservation_units.models import ReservationUnit
from reservations.forms import ReservationForm
from reservations.models import Reservation
from resources.models import Resource
from services.models import Service
from spaces.models import Building, District, RealEstate, Space


class ServiceType(DjangoObjectType):
    buffer_time_before = graphene.String()
    buffer_time_after = graphene.String()

    class Meta:
        model = Service
        fields = (
            "id",
            "name",
            "service_type",
            "buffer_time_before",
            "buffer_time_after",
        )


class DistrictType(DjangoObjectType):
    class Meta:
        model = District
        fields = ("id", "name")


class RealEstateType(DjangoObjectType):
    class Meta:
        model = RealEstate
        fields = ("id", "name", "district", "area")


class BuildingType(DjangoObjectType):
    district = DistrictType()
    real_estate = RealEstateType()

    class Meta:
        model = Building
        fields = ("id", "name", "district", "real_estate", "area")


class SpaceType(DjangoObjectType):
    class Meta:
        model = Space
        fields = (
            "id",
            "name",
            "parent",
            "building",
            "area",
        )


class ResourceType(DjangoObjectType):
    building = graphene.List(BuildingType)

    class Meta:
        model = Resource
        fields = (
            "id",
            "location_type",
            "name",
            "space",
            "buffer_time_before",
            "buffer_time_after",
        )


class ReservationUnitType(AuthNode, DjangoObjectType):
    spaces = graphene.List(SpaceType)
    resources = graphene.List(ResourceType)
    location = graphene.String()


    class Meta:
        model = ReservationUnit
        fields = (
            "id",
            "name",
            "spaces",
            "resources",
            "services",
            "require_introduction",
        )
        filter_fields = ("name", "spaces", "resources", "services", "require_introduction")
        interfaces = (relay.Node,)

    def resolve_spaces(self, info):
        return Space.objects.filter(reservation_units=self.id).select_related(
            "parent", "building"
        )

    def resolve_resources(self, info):
        return Resource.objects.filter(reservation_units=self.id)

    def resolve_location(self, info):
        location = self.get_location()
        return location


class ReservationType(DjangoObjectType):
    class Meta:
        model = Reservation


class ReservationMutation(DjangoModelFormMutation):
    reservation = graphene.Field(ReservationType)

    class Meta:
        form_class = ReservationForm

class AllowAuthenticatedFilter(AuthFilter):
    permission_classes = (AllowAuthenticated,)


class Query(graphene.ObjectType):
    # ressu = relay.Node.Field(ReservationUnitType)
    # all_reservation_units = AllowAuthenticatedFilter(ReservationUnitType)
    all_reservation_units = DjangoFilterConnectionField(ReservationUnitType)
    reservation_unit = graphene.Field(
        ReservationUnitType, reservation_unit_id=graphene.Int()
    )
    reservation_unit_query = graphene.List(
        ReservationUnitType, reservation_unit_name=graphene.String()
    )

    # def resolve_all_reservation_units(root, info):
    #     return ReservationUnit.objects.all().prefetch_related(
    #         "spaces", "resources", "services"
    #     )

    def resolve_reservation_unit(self, info, reservation_unit_id):
        return ReservationUnit.objects.get(id=reservation_unit_id)

    def resolve_reservation_unit_query(self, info, reservation_unit_name):
        return ReservationUnit.objects.filter(name=reservation_unit_name)


class Mutation(graphene.ObjectType):
    create_reservation = ReservationMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
