from rest_framework.permissions import BasePermission


class IsAdminOrEmployer(BasePermission):
    """
    Allows only Admins or Employers to create resources.
    """

    message = "Only Admins or Employers can perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.is_admin() or request.user.is_employer()
        )


class IsAdminOrResourceOwner(BasePermission):
    """
    Allows modification only by Admins or resource owners.
    """

    message = "You must be an Admin or the resource owner to perform this action."

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.is_admin() or getattr(obj, "created_by", None) == request.user
        )
