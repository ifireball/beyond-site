"""Tests for the tooling_challenge app views"""
from typing import Final
from uuid import UUID

import pytest
from django.test import Client

from ..forms import SubmissionForm

SUBMISSION_FORM_PATH: Final[str] = "/tooling_challenge/submission_form"
SUBMISSION_STATUS_PATH: Final[str] = "/tooling_challenge/submission_status"


def test_submission_form_get(client: Client) -> None:
    """
    Test that simple HTTP get to the submission form displays an empty form.
    """
    response = client.get(SUBMISSION_FORM_PATH)

    assert response.status_code == 200
    template_names = [tmpl.origin.template_name for tmpl in response.templates[0:1]]
    assert template_names == ["tooling_challenge/submission_form.html"]
    form = response.context["form"]
    assert isinstance(form, SubmissionForm)
    assert not form.is_bound


@pytest.mark.parametrize(
    "post_data",
    [
        pytest.param({}, id="Empty form"),
        pytest.param({"name": "John Doe"}, id="Only name"),
        pytest.param({"email": "foo@bar.com"}, id="Only email"),
        pytest.param({"url": "https://bar.com/foo"}, id="Only url"),
        pytest.param({"name": "John Doe", "email": "foo@bar.com"}, id="name & email"),
        pytest.param(
            {"name": "John Doe", "url": "https://bar.com/foo"}, id="name & url"
        ),
        pytest.param(
            {"email": "foo@bar.com", "url": "https://bar.com/foo"}, id="email & url"
        ),
        pytest.param(
            {"name": "John Doe", "email": "for", "url": "https://bar.com/foo"},
            id="invalid email",
        ),
        pytest.param(
            {"name": "John Doe", "email": "foo@bar.com", "url": "foo"}, id="invalid url"
        ),
    ],
)
@pytest.mark.django_db
def test_submission_form_invalid_post(client: Client, post_data: dict) -> None:
    """
    Test error responses when invalid data is submitted
    """
    response = client.post(SUBMISSION_FORM_PATH, post_data)

    assert response.status_code == 200
    template_names = [tmpl.origin.template_name for tmpl in response.templates[0:1]]
    assert template_names == ["tooling_challenge/submission_form.html"]
    form = response.context["form"]
    assert isinstance(form, SubmissionForm)
    assert form.is_bound
    assert not form.is_valid()
    assert form.data.dict() == post_data


@pytest.mark.django_db
def test_submission_form_valid_post(client: Client) -> None:
    """
    Test behaviour when valid data is posted
    """
    post_data = {
        "name": "John Doe",
        "email": "foo@bar.com",
        "url": "https://bar.com/foo",
    }
    response = client.post(SUBMISSION_FORM_PATH, post_data)

    assert response.status_code == 302


# @pytest.mark.django_db
def test_submission_status(client: Client) -> None:
    """
    Thst that the sumbission status page shows the status of an existing
    submission
    """
    submission_status_uuid = UUID("12345678-90ab-cdef-1234-567890abcdef")
    submssion_status_path = f"{SUBMISSION_STATUS_PATH}/{submission_status_uuid}"
    response = client.get(submssion_status_path)

    assert response.status_code == 200
    template_names = [tmpl.origin.template_name for tmpl in response.templates[0:1]]
    assert template_names == ["tooling_challenge/submission_status.html"]
