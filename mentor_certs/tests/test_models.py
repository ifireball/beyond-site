"""Tests for mentor_certs models"""
from __future__ import annotations

from itertools import chain, repeat

import pytest
from more_itertools import triplewise

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


@pytest.mark.django_db
@pytest.mark.parametrize(
    "course, certnames",
    (
        pytest.param(*args, id=f"{args[0]}-{args[1][1]}")
        for args in chain(
            zip(
                repeat("Beyond OS 06"),
                triplewise((None, "Barak Korren", "Kobi Hakimi", "Omer Amsalem", None)),
            ),
            zip(
                repeat("Beyond Cyber 01"),
                triplewise((None, "Haim Krasniker", "Luiza Nachshon", None)),
            ),
        )
    ),
)
def test_navigation(course: str, certnames: tuple[str, str, str]) -> None:
    """Test Certificate navigation properties:
    * nav_next     - points to the next certificate in the same course ordered
                     lexicographically by staff_member name or None if its the
                     last one
    * nav_previous - points to the previous certificate in the same course
                     ordered lexicographically by staff_member name or None if
                     its the first one
    """
    previous, current, nextcert = (
        Certificate.certificates.get(course__name=course, staff_member__name=certname)
        if certname
        else None
        for certname in certnames
    )

    assert current.nav_previous == previous
    assert current.nav_next == nextcert
