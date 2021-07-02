from graphene_permissions.permissions import BasePermission as GrapheneBasePermission
from graphql import ResolveInfo
from rest_framework.permissions import BasePermission as DRFBasePermission


class ApiPermissionGrapheneBase(GrapheneBasePermission):
    drf_class = None

    @classmethod
    def has_node_permission(self, info: ResolveInfo, id: str):
        self.has_permission()

    @classmethod
    def has_mutation_permission(self, root, info: ResolveInfo, input: dict):
        return self.has_object_permission()

    @classmethod
    def has_filter_permission(self, info: ResolveInfo):
        """For regular request the info's context should be wsgi request object. So we can pass it to drf permission check.

        The view obviously does not exist and is needed to be handled in drf permission class.

        One big thing to tackle with is that this is class based :S so the latest .for_graphql() call will override the previous.


        """
        return self.drf_class.has_permission(info.context, None)


class ApiPermissionsBase(DRFBasePermission):
    @classmethod
    def for_graphql(cls):
        ApiPermissionGrapheneBase.drf_class = cls
        return ApiPermissionGrapheneBase