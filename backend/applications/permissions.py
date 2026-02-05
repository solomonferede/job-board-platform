from rest_framework.permissions import BasePermission

from jobs.models import Job


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
    Check if the user is the owner of the job.
    - For list views, checks the job's ownership via `job_pk` from the URL.
    - For detail views, checks ownership via the application object's related job.
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated or not request.user.is_employer():
            return False

        # Check for job_pk for list views (e.g., /jobs/{job_pk}/applications/)
        if "job_pk" in view.kwargs:
            job_pk = view.kwargs["job_pk"]
            try:
                job = Job.objects.get(pk=job_pk)
                return job.created_by == request.user
            except Job.DoesNotExist:
                return False

        # Defer to has_object_permission for detail views where there's no job_pk in the URL kwargs
        return True

    def has_object_permission(self, request, view, obj):
        # This is for endpoints where the object is an Application (e.g., /applications/{app_pk}/)
        if not request.user.is_authenticated or not request.user.is_employer():
            return False

        return obj.job.created_by == request.user
