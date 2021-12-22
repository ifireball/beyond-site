"""Tests for the tooling_challenge app views"""
from typing import Final
from uuid import UUID

import pytest
from django.test import Client

from ..forms import SubmissionForm
from ..models import ToolingChallengeSubmission

SUBMISSION_FORM_PATH: Final[str] = "/tooling_challenge/submission_form"
SUBMISSION_ROOT_PATH: Final[str] = "/tooling_challenge/submission"


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
        pytest.param({"repo_url": "https://bar.com/foo"}, id="Only url"),
        pytest.param({"name": "John Doe", "email": "foo@bar.com"}, id="name & email"),
        pytest.param(
            {"name": "John Doe", "repo_url": "https://bar.com/foo"}, id="name & url"
        ),
        pytest.param(
            {"email": "foo@bar.com", "repo_url": "https://bar.com/foo"},
            id="email & url",
        ),
        pytest.param(
            {"name": "John Doe", "email": "foo", "repo_url": "https://bar.com/foo"},
            id="invalid email",
        ),
        pytest.param(
            {"name": "John Doe", "email": "foo@bar.com", "repo_url": "foo"},
            id="invalid url",
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
    some_name = "John Doe"
    some_email = "foo@bar.com"
    some_repo_url = "https://bar.com/foo"
    post_data = {"name": some_name, "email": some_email, "repo_url": some_repo_url}

    response = client.post(SUBMISSION_FORM_PATH, post_data)

    assert response.status_code == 302
    submission_path_prefix = f"{SUBMISSION_ROOT_PATH}/"
    assert response.url.startswith(submission_path_prefix)
    submission_uuid_str = response.url[len(submission_path_prefix) :]
    submission_uuid = UUID(submission_uuid_str)
    submission = ToolingChallengeSubmission.submissions.get(uuid=submission_uuid)
    assert submission.name == some_name
    assert submission.email == some_email
    assert submission.repo_url == some_repo_url


# @pytest.mark.django_db
def test_submission_status(client: Client) -> None:
    """
    Thst that the sumbission status page shows the status of an existing
    submission
    """
    submission_uuid = UUID("12345678-90ab-cdef-1234-567890abcdef")
    submssion_status_path = f"{SUBMISSION_ROOT_PATH}/{submission_uuid}"
    response = client.get(submssion_status_path)

    assert response.status_code == 200
    template_names = [tmpl.origin.template_name for tmpl in response.templates[0:1]]
    assert template_names == ["tooling_challenge/submission_status.html"]
