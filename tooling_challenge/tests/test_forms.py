"""Tests for the tooling_challenge app forms"""
from ..forms import SubmissionForm


def test_submssion_form_fields() -> None:
    """Test that the submission for displays the right set of fields"""
    form = SubmissionForm()
    fields = [(field.name, field.widget_type) for field in form]

    assert fields == [
        ("name", "text"),
        ("email", "email"),
        ("repo_url", "url"),
    ]
