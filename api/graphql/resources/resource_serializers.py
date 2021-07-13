from api.graphql.base_serializers import (
    PrimaryKeySerializer,
    PrimaryKeyUpdateSerializer,
)
from api.resources_api import ResourceSerializer


class ResourceCreateSerializer(ResourceSerializer, PrimaryKeySerializer):
    class Meta(ResourceSerializer.Meta):
        fields = [
            field
            for field in ResourceSerializer.Meta.fields
            if field != "location_type"
        ] + ["pk"]


class ResourceUpdateSerializer(ResourceSerializer, PrimaryKeyUpdateSerializer):
    class Meta(ResourceCreateSerializer.Meta):
        fields = ResourceCreateSerializer.Meta.fields + ["pk"]
