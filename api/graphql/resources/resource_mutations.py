import graphene
from graphene_django.rest_framework.mutation import SerializerMutation
from graphene_django_extras import DjangoSerializerMutation
from rest_framework.generics import get_object_or_404

from api.graphql.resources.resource_serializers import (
    ResourceCreateSerializer,
    ResourceUpdateSerializer,
)
from api.graphql.resources.resource_types import ResourceType
from resources.models import Resource


class ResourceCreateMutation(DjangoSerializerMutation):
    resource = graphene.Field(ResourceType)

    class Meta:
        model_operations = ["create"]

        serializer_class = ResourceCreateSerializer

    @classmethod
    def perform_mutate(cls, serializer, info):
        purpose = serializer.create(serializer.validated_data)
        return cls(errors=None, purpose=purpose)


class ResourceUpdateMutation(DjangoSerializerMutation):
    resource = graphene.Field(ResourceType)

    class Meta:
        model_operations = ["update"]
        lookup_field = "pk"
        serializer_class = ResourceUpdateSerializer

    @classmethod
    def perform_mutate(cls, serializer, info):

        validated_data = serializer.validated_data
        pk = validated_data.get("pk")
        purpose = serializer.update(get_object_or_404(Resource, pk=pk), validated_data)
        return cls(errors=None, purpose=purpose)
