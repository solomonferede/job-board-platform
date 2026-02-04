from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    message = "You must be an admin user to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class IsEmployer(BasePermission):
    """
    Allows access only to employer users.
    """

    message = "You must be an employer user to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_employer()
