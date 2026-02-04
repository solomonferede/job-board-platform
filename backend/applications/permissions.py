from rest_framework.permissions import BasePermission


class IsJobSeeker(BasePermission):
    """
    Allows access only to authenticated job seekers.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_job_seeker()


class IsEmployerOwner(BasePermission):
    """
    Allows access only to the employer who created the job
    related to the application.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.is_employer()
            and obj.job.created_by == request.user
        )


class IsAdmin(BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin()
