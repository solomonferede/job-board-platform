from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow read-only access to any user,
    but write access only to admin users.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and request.user.is_admin()


class IsAdminOrOwnerOrReadOnly(BasePermission):
    """
    Custom permission to only allow owners of an object or admins to edit it.
    Read-only access is allowed for everyone.
    """

    def has_permission(self, request, view):
        # Allow all GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Allow POST requests only for authenticated users (employers).
        # The check to limit to one company will be in the view's create method.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow all GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the company or an admin.
        # Assumes the model instance has a `created_by` attribute.
        return obj.created_by == request.user or (request.user and request.user.is_authenticated and request.user.is_admin())


class IsAdminOrEmployer(BasePermission):
    """
    Allows access only to admin or employer users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_admin() or request.user.is_employer())


class IsAdminOrResourceOwner(BasePermission):
    """
    Allows access only to admin users or the owner of the resource.
    Assumes the object has a 'created_by' field.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user and request.user.is_authenticated and request.user.is_admin()
        ) or (obj.created_by == request.user)