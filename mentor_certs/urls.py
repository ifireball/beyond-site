"""mentor_certs app URLs"""
from django.urls import path

from .view_names import CERTIFICATE_PDF, CERTIFICATE_VIEW
from .views import certificate_pdf, certificate_view, root

urlpatterns = [
    path("", root),
    path("certificate/<int:certificate_id>", certificate_view, name=CERTIFICATE_VIEW),
    path("certificate/<int:certificate_id>.pdf", certificate_pdf, name=CERTIFICATE_PDF),
]
