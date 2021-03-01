from django_graphene_permissions import PermissionDenied
from django_graphene_permissions.permissions import BasePermission, PermissionDjangoObjectType


class SuperuserPermission(BasePermission):

    @staticmethod
    def has_permission(context):
        return all([
            context.user,
            context.user.is_authenticated,
            context.user.is_superuser,
        ])

    @staticmethod
    def has_object_permission(context, obj):
        return True


class PetOwnerPermission(BasePermission):

    @staticmethod
    def has_permission(context):
        return all([
            context.user,
            context.user.is_authenticated,
            context.user.profile.__class__.__name__ == 'PetOwner',
        ])

    @staticmethod
    def has_object_permission(context, obj):
        return True


class PracticeStaffPermission(BasePermission):

    @staticmethod
    def has_permission(context):
        return all([
            context.user,
            context.user.is_authenticated,
            context.user.profile.__class__.__name__ in ['PracticeStaff', 'Vet', 'PracticeManager'],
        ])

    @staticmethod
    def has_object_permission(context, obj):
        return True


class PracticeManagerPermission(BasePermission):

    @staticmethod
    def has_permission(context):
        return all([
            context.user,
            context.user.is_authenticated,
            context.user.profile.__class__.__name__ == 'PracticeManager',
        ])

    @staticmethod
    def has_object_permission(context, obj):
        return True


class VetPermission(BasePermission):

    @staticmethod
    def has_permission(context):
        return all([
            context.user,
            context.user.is_authenticated,
            context.user.profile.__class__.__name__ == 'Vet',
        ])

    @staticmethod
    def has_object_permission(context, obj):
        return True


class RoleFilterNodeMixin():
    """for user role's request, do the filter to control the visibility"""
    role_filters = {}

    @classmethod
    def get_role_name(cls, info):
        # PetOwner / PracticeManager/ Vet
        if getattr(info.context, 'profile', None):
            return info.context.profile.__class__.__name__

        return None

    @classmethod
    def filter_queryset(cls, queryset, info):
        if info.context.user.is_superuser:
            # super user return all
            return queryset
        elif info.context.user.is_anonymous:
            # anonymous raise 403
            raise PermissionDenied

        role_name = cls.get_role_name(info)

        if role_name and cls.role_filters:
            query_field = cls.role_filters.get(role_name)
            if query_field:
                return queryset.filter(**{query_field: info.context.profile.id})

        raise PermissionDenied
