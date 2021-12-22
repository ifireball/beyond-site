"""tooling_challenge app urls"""
from django.urls import path

from .view_names import SUMBISSION_VIEW
from .views import submission_form, submission_status

urlpatterns = [
    path("submission_form", submission_form),
    path(
        "submission/<uuid:submission_uuid>",
        submission_status,
        name=SUMBISSION_VIEW,
    ),
]
