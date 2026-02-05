from rest_framework.permissions import BasePermission


class IsApplicantOwner(BasePermission):
    """
    Allows access only to the user who created the application.
    """

    def has_object_permission(self, request, view, obj):
        return obj.applicant == request.user


class IsJobSeeker(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_job_seeker()


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_employer()


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()


class IsJobOwner(BasePermission):
    """
    Check if the user is the owner of the job associated with the application.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_employer()
            and obj.job.created_by == request.user
        )