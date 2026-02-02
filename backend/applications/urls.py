from django.urls import path
from .views import (
    ApplyJobView,
    MyApplicationsView,
    WithdrawApplicationView,
    JobApplicationsView,
    UpdateApplicationStatusView,
    AdminAllApplicationsView,
)

urlpatterns = [
    path("", ApplyJobView.as_view()),
    path("my/", MyApplicationsView.as_view()),
    path("<int:pk>/withdraw/", WithdrawApplicationView.as_view()),
    path("job/<int:job_id>/", JobApplicationsView.as_view()),
    path("<int:pk>/status/", UpdateApplicationStatusView.as_view()),
    path("admin/all/", AdminAllApplicationsView.as_view()),
]
