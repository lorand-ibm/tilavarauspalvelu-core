from typing import Union

import graphene
from easy_thumbnails.files import get_thumbnailer
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.forms.mutation import DjangoModelFormMutation
from graphene_permissions.mixins import AuthFilter, AuthNode
from graphene_permissions.permissions import AllowAuthenticated

from reservation_units.models import ReservationUnit, Purpose, ReservationUnitImage
from reservations.forms import ReservationForm
from reservations.models import Reservation
from resources.models import Resource
from services.models import Service
from spaces.models import Building, District, RealEstate, Space, Location


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
class PurposeType(DjangoObjectType):
    class Meta:
        model = Purpose
        fields = (
            "id",
            "name",

        )

class ReservationUnitImageType(DjangoObjectType):
    image_url = graphene.String()
    medium_url = graphene.String()
    small_url = graphene.String()

    class Meta:
        model = ReservationUnitImage
        fields = ["image_url", "medium_url", "small_url", "image_type"]

    def resolve_image_url(self, info):
        if not self.image:
            return None
        return info.context.build_absolute_uri(self.image.url)

    def resolve_small_url(self, info):
        if not self.image:
            return None
        url = get_thumbnailer(self.image)["small"].url

        return info.context.build_absolute_uri(url)

    def resolve_medium_url(self, info):
        if not self.image:
            return None
        url = get_thumbnailer(self.image)["medium"].url

        return info.context.build_absolute_uri(url)
# class ReservationUnitSerializer(TranslatedModelSerializer):
#     spaces = SpaceSerializer(
#         read_only=True,
#         many=True,
#         help_text="Spaces included in the reservation unit as nested related objects.",
#     )
#     resources = ResourceSerializer(
#         read_only=True,
#         many=True,
#         help_text="Resources included in the reservation unit as nested related objects.",
#     )
#     services = ServiceSerializer(
#         read_only=True,
#         many=True,
#         help_text="Services included in the reservation unit as nested related objects.",
#     )
#     purposes = PurposeSerializer(many=True, read_only=True)
#     images = ReservationUnitImageSerializer(
#         read_only=True,
#         many=True,
#         help_text="Images of the reservation unit as nested related objects. ",
#     )
#     location = serializers.SerializerMethodField(
#         help_text="Location of this reservation unit. Dynamically determined from spaces of the reservation unit."
#     )
#     max_persons = serializers.SerializerMethodField(
#         help_text="Max persons that are allowed in this reservation unit simultaneously."
#     )
#     building = serializers.SerializerMethodField()
#     reservation_unit_type = ReservationUnitTypeSerializer(
#         read_only=True,
#         help_text="Type of the reservation unit as nested related object.",
#     )
#
#     equipment_ids = serializers.PrimaryKeyRelatedField(
#         queryset=Equipment.objects.all(),
#         source="equipments",
#         many=True,
#         help_text="Ids of equipment available in this reservation unit.",
#     )
#
#     unit_id = serializers.PrimaryKeyRelatedField(
#         queryset=Unit.objects.all(), source="unit"
#     )
#
#     uuid = serializers.UUIDField(read_only=True)
#
#     class Meta:
#         model = ReservationUnit
#         fields = [
#             "id",
#             "name",
#             "description",
#             "spaces",
#             "resources",
#             "services",
#             "require_introduction",
#             "purposes",
#             "images",
#             "location",
#             "max_persons",
#             "reservation_unit_type",
#             "building",
#             "terms_of_use",
#             "equipment_ids",
#             "unit_id",
#             "uuid",
#             "contact_information",
#         ]


class LocationType(DjangoObjectType):
    longitude = graphene.String()
    latitude = graphene.String()


    def resolve_longitude(self, obj):
        return self.lon
    
    def resolve_latitude(self, obj):
        return self.lat

    class Meta:
        model = Location
        fields = ["address_street", "address_zip", "address_city","longitude", "latitude"]

class ReservationUnitType(AuthNode, DjangoObjectType):
    spaces = graphene.List(SpaceType)
    resources = graphene.List(ResourceType)
    location = graphene.String()
    purposes = graphene.List(PurposeType)
    images = graphene.List(ReservationUnitImageType)
    location = graphene.Field(LocationType)

    class Meta:
        model = ReservationUnit
        fields = (
            "id",
            "name",
            "description",
            "spaces",
            "resources",
            "services",
            "require_introduction",
                        "purposes"
                        "images",
                        "location",
                        # "max_persons",
                        # "reservation_unit_type",
                        # "building",
                        # "terms_of_use",
                        # "equipment_ids",
                        # "unit_id",
                        # "uuid",
                        # "contact_information",

        )
        filter_fields = {
            'name': ['exact', 'icontains', 'istartswith'],
        }

        interfaces = (relay.Node,)

    def resolve_location(self, info):
        return self.get_location()

    def resolve_spaces(self, info):
        return Space.objects.filter(reservation_units=self.id).select_related(
            "parent", "building"
        )

    def resolve_purposes(self, info):
        return Purpose.objects.filter(reservation_units=self.id)

    def resolve_images(self, info):
        return ReservationUnitImage.objects.filter(reservation_unit_id=self.id)

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
    all_reservation_units = DjangoFilterConnectionField(ReservationUnitType)#graphene.List(ReservationUnitType)
    reservation_unit = graphene.Field(
        ReservationUnitType, reservation_unit_id=graphene.Int()
    )
    reservation_unit_query = graphene.List(
        ReservationUnitType, reservation_unit_name=graphene.String()
    )

    #def resolve_all_reservation_units(root, info):
    #    return ReservationUnit.objects.all().prefetch_related(
    #        "spaces", "resources", "services"
    #    )

    def resolve_reservation_unit(self, info, reservation_unit_id):
        return ReservationUnit.objects.get(id=reservation_unit_id)

    def resolve_reservation_unit_query(self, info, reservation_unit_name):
        return ReservationUnit.objects.filter(name=reservation_unit_name)


class Mutation(graphene.ObjectType):
    create_reservation = ReservationMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
