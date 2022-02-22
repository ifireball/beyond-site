"""mentor_certs views"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from .models import Certificate


def root(request: HttpRequest) -> HttpResponse:
    """The app root view - redirects to the default certificate"""
    return redirect(Certificate.certificates.default)


def certificate_view(request: HttpRequest, *, certificate_id: int) -> HttpResponse:
    """Display a certificate"""
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    return TemplateResponse(
        request, "mentor_certs/certificate_view.html", {"certificate": certificate}
    )
