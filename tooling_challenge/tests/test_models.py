"""tooling_challenge model tests"""
from __future__ import annotations

from random import choice

import pytest

from ..models import ToolingChallengeSubmission


@pytest.fixture
def some_submissions() -> list[ToolingChallengeSubmission]:
    """Create some sample ToolingChallengeSubmission objects"""
    submissions = [
        ToolingChallengeSubmission(
            name="Howl",
            email="howl@wisards.org",
            repo_url="https://github.com/howl/challnge1.git",
        ),
        ToolingChallengeSubmission(
            name="Sophie Hatter",
            email="sophie@hatters.com",
            repo_url="https://hatters.com/sophie/ch1.git",
        ),
        ToolingChallengeSubmission(
            name="Lattie Hatter",
            email="lattie@hatters.com",
            repo_url="https://hatters.com/lattie/ch1.git",
        ),
    ]
    for submssion in submissions:
        submssion.save()
    return submissions


@pytest.mark.django_db
def test_submission_by_uuid(some_submissions: list[ToolingChallengeSubmission]):
    """Test fetching a submission by its UUID"""
    chosen_submission = choice(some_submissions)
    chosen_uuid = chosen_submission.uuid

    gotten_submission = ToolingChallengeSubmission.submissions.get(uuid=chosen_uuid)

    assert gotten_submission == chosen_submission


@pytest.mark.django_db
def test_new_submission_triggers_url_test():
    """That that crating a submission triggers a test of its repo URL"""
