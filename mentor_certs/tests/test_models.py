"""Tests for mentor_certs models"""
import pytest

from ..models import Certificate


@pytest.mark.django_db
def test_default_cert() -> None:
    """
    Fetching the default certificate gives you the one for the first staff
    memebr (lexicographically ordered) form the most recently ended course
    """
    bkorren_06_cert = Certificate.certificates.get(
        course__name="Beyond OS 06", staff_member__name="Barak Korren"
    )

    default_cert = Certificate.certificates.default

    assert bkorren_06_cert == default_cert
