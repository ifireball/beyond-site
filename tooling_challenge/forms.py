"""tooling_challenge forms"""
from django.forms import ModelForm

from .models import ToolingChallengeSubmission


class SubmissionForm(ModelForm):
    """Forms for submitting challenge responses"""

    class Meta:
        model = ToolingChallengeSubmission
        fields = ["name", "email", "repo_url"]
