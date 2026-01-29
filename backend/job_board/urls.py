from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # API v1
    path("api/v1/accounts/", include("accounts.urls")),
    path("api/v1/jobs/", include("jobs.urls")),
]
