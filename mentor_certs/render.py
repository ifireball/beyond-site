"""Rendering routines for mentor certificates"""
from django.template.loader import render_to_string
from lxml.etree import XMLParser, fromstring  # pylint: disable=no-name-in-module
from reportlab.graphics import renderPDF
from svglib.svglib import SvgRenderer

from .models import Certificate


def svg(certificate: Certificate) -> str:
    """Render a certificate to SVG"""
    return render_to_string(
        "mentor_certs/certificate.svg",
        {
            "certificate": certificate,
            "cert_name": certificate.staff_member.name,
            "cert_date": certificate.course.end_date,
        },
    )


def pdf(certificate: Certificate) -> str:
    """Renders a certificate to PDF"""
    xml_parser = XMLParser(remove_comments=True, recover=True)
    svg_tree = fromstring(svg(certificate).encode(), xml_parser)
    svg_renderer = SvgRenderer(f"{certificate.pk}.svg")
    rendered_svg = svg_renderer.render(svg_tree)
    return renderPDF.drawToString(rendered_svg)
