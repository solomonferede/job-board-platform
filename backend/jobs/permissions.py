from rest_framework.permissions import BasePermission


class IsAdminOrEmployer(BasePermission):
    """
    Only Admins or Employers can create/update/delete jobs.
    """
    message = "You must be an Admin or Employer to perform this action."

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_admin() or request.user.is_employer())
        )


class IsJobSeekerOrReadOnly(BasePermission):
    """
    Job seekers can view jobs but cannot create/update/delete.
    """
    message = "You must be a Job Seeker or have read-only access."

    def has_permission(self, request, view):
        if request.method in ("GET", "HEAD", "OPTIONS"):
            return True
        return False
