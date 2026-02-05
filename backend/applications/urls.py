from django.urls import path

from .views import (
    ApplicationDetailView,
    MyApplicationListView,
)

urlpatterns = [
    path(
        "my-applications/",
        MyApplicationListView.as_view(),
        name="my-application-list",
    ),
    path(
        "<int:pk>/",
        ApplicationDetailView.as_view(),
        name="application-detail",
    ),
]
