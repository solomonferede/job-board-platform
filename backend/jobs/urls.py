from django.urls import path
from applications.views import JobApplicationListCreateView

from jobs.views.category_views import (
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
)
from jobs.views.company_views import (
    CompanyListCreateView,
    CompanyRetrieveUpdateDestroyView,
)
from jobs.views.job_type_views import (
    JobTypeListCreateView,
    JobTypeRetrieveUpdateDestroyView,
)
from jobs.views.job_views import (
    JobListCreateView,
    JobRetrieveUpdateDestroyView,
)
from jobs.views.location_views import (
    LocationListCreateView,
    LocationRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Jobs
    path("", JobListCreateView.as_view(), name="job-list-create"),
    path("<int:id>/", JobRetrieveUpdateDestroyView.as_view(), name="job-detail"),
    # Job Applications (Nested)
    path(
        "<int:job_pk>/applications/",
        JobApplicationListCreateView.as_view(),
        name="job-application-list-create",
    ),
    # Categories
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path(
        "categories/<int:id>/",
        CategoryRetrieveUpdateDestroyView.as_view(),
        name="category-detail",
    ),
    # Job Types
    path("job-types/", JobTypeListCreateView.as_view(), name="jobtype-list-create"),
    path(
        "job-types/<int:id>/",
        JobTypeRetrieveUpdateDestroyView.as_view(),
        name="jobtype-detail",
    ),
    # Locations
    path("locations/", LocationListCreateView.as_view(), name="location-list-create"),
    path(
        "locations/<int:id>/",
        LocationRetrieveUpdateDestroyView.as_view(),
        name="location-detail",
    ),
    # Companies
    path("companies/", CompanyListCreateView.as_view(), name="company-list-create"),
    path(
        "companies/<int:id>/",
        CompanyRetrieveUpdateDestroyView.as_view(),
        name="company-detail",
    ),
]
