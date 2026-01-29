from django.urls import path
from .views import (
    JobListCreateView,
    JobRetrieveUpdateDestroyView,
    CategoryListCreateView,
    CategoryRetrieveUpdateDestroyView,
    JobTypeListCreateView,
    JobTypeRetrieveUpdateDestroyView,
    LocationListCreateView,
    LocationRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Jobs
    path("", JobListCreateView.as_view(), name="job-list-create"),
    path("<int:id>/", JobRetrieveUpdateDestroyView.as_view(), name="job-detail"),

    # Categories
    path("categories/", CategoryListCreateView.as_view(), name="category-list-create"),
    path("categories/<int:id>/", CategoryRetrieveUpdateDestroyView.as_view(), name="category-detail"),

    # Job Types
    path("job-types/", JobTypeListCreateView.as_view(), name="jobtype-list-create"),
    path("job-types/<int:id>/", JobTypeRetrieveUpdateDestroyView.as_view(), name="jobtype-detail"),

    # Locations
    path("locations/", LocationListCreateView.as_view(), name="location-list-create"),
    path("locations/<int:id>/", LocationRetrieveUpdateDestroyView.as_view(), name="location-detail"),
]
