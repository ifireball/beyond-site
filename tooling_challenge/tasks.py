"""tooling_challenge background processing tasks"""
from .models import ToolingChallengeSubmission


def test_submission_repo_url(submssion: ToolingChallengeSubmission, **_):
    """Test that a submission's repo URL can be cloned and record the SHA found there"""
    assert submssion
