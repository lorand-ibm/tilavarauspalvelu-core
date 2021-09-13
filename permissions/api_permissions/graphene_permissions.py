from typing import Any

from graphene_permissions.permissions import BasePermission
from graphql import ResolveInfo

from permissions.helpers import (
    can_create_reservation,
    can_manage_purposes,
    can_manage_resources,
    can_manage_spaces,
    can_manage_units,
    can_manage_units_reservation_units,
    can_view_reservations,
)
from reservations.models import Reservation
from spaces.models import Unit

class PrimaryKeyResolvableBasePermission(BasePermission):
    @classmethod
    def has_node_permission_by_pk(cls, info: ResolveInfo, pk: str) -> bool:
        return cls.has_permission(info)


class ReservationUnitHaukiUrlPermission(PrimaryKeyResolvableBasePermission):
    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        return False

    @classmethod
    def has_node_permission_by_pk(cls, info: ResolveInfo, id: str) -> bool:
        # FIXME: needs a fix for permissions, not called currently TILA-777
        return True

    @classmethod
    def has_mutation_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        return False


class ReservationUnitPermission(PrimaryKeyResolvableBasePermission):
    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        return True

    @classmethod
    def has_primary_key_permission(cls, info: ResolveInfo, pk: int) -> bool:
        return cls.has_permission(info)

    @classmethod
    def has_mutation_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        unit = Unit.objects.filter(id=input["unit_id"]).first()
        return can_manage_units_reservation_units(info.context.user, unit)


class ResourcePermission(PrimaryKeyResolvableBasePermission):
    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        return True

    @classmethod
    def has_node_permission(cls, info: ResolveInfo, id: str) -> bool:
        return True

    @classmethod
    def has_mutation_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        return can_manage_resources(info.context.user)


class ReservationPermission(PrimaryKeyResolvableBasePermission):
    @classmethod
    def has_mutation_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        reservation = Reservation(**input)
        return can_create_reservation(info.context.user, reservation)

    @classmethod
    def has_filter_permission(self, info: ResolveInfo) -> bool:
        return can_view_reservations(info.context.user)


class PurposePermission(PrimaryKeyResolvableBasePermission):
    @classmethod
    def has_filter_permission(cls, info: ResolveInfo) -> bool:
        return True

    @classmethod
    def has_mutation_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        return can_manage_purposes(info.context.user)


class SpacePermission(PrimaryKeyResolvableBasePermission):
    @classmethod
    def has_permission(cls, info: ResolveInfo) -> bool:
        return True

    @classmethod
    def has_filter_permission(cls, info: ResolveInfo) -> bool:
        return True

    @classmethod
    def has_mutation_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        return can_manage_spaces(info.context.user)


class UnitPermission(PrimaryKeyResolvableBasePermission):
    def has_permission(cls, info: ResolveInfo) -> bool:
        return True

    @classmethod
    def has_mutation_permission(cls, root: Any, info: ResolveInfo, input: dict) -> bool:
        return can_manage_units(info.context.user)
