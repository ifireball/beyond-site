"""
Tests for mentor_certs app views
"""
from random import choice

import pytest
from django.test import Client

from mentor_certs.models import Certificate


@pytest.mark.django_db
def test_default_redircet(client: Client) -> None:
    """Test the the app root redirects to the default certificate"""
    default_cert = Certificate.certificates.default
    expected_path = f"/mentor_certs/certificate/{default_cert.pk}"

    response = client.get("/mentor_certs/")

    assert response.status_code == 302
    assert response.url == expected_path


@pytest.mark.django_db
def test_certificate_view(client: Client) -> None:
    """Test that the certificate view displays the asked-for certificate"""
    some_cert = choice(Certificate.certificates.all())

    response = client.get(f"/mentor_certs/certificate/{some_cert.pk}")

    assert response.status_code == 200
    template_names = [tmpl.origin.template_name for tmpl in response.templates[0:1]]
    assert template_names == ["mentor_certs/certificate_view.html"]
    shown_cert = response.context["certificate"]
    assert shown_cert == some_cert
