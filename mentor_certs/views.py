"""mentor_certs views"""
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from lxml.etree import XMLParser, fromstring  # pylint: disable=no-name-in-module
from reportlab.graphics import renderPDF
from svglib.svglib import SvgRenderer

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


def certificate_pdf(request: HttpRequest, *, certificate_id: int) -> HttpResponse:
    """Retrive a certificate PDF file"""
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    svg_response = TemplateResponse(
        request,
        "mentor_certs/certificate.svg",
        {
            "certificate": certificate,
            "cert_name": certificate.staff_member.name,
            "cert_date": certificate.course.end_date,
        },
    )
    svg_response.render()
    xml_parser = XMLParser(remove_comments=True, recover=True)
    svg_tree = fromstring(svg_response.content, xml_parser)
    svg_renderer = SvgRenderer(f"{certificate.pk}.svg")
    rendered_svg = svg_renderer.render(svg_tree)
    response = HttpResponse(
        renderPDF.drawToString(rendered_svg),
        headers={
            "Content-Type": "application/pdf",
            "Content-Disposition": f'attachment; filename="{certificate.pk}.pdf"',
        },
    )
    return response
