"""tooling_challenge models"""
from __future__ import annotations

import uuid

from django.db import models
from django.urls import reverse

from .view_names import SUMBISSION_VIEW


class ToolingChallengeSubmission(models.Model):
    """Store subitted challenge results"""

    name = models.CharField(max_length=255, blank=False, null=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    repo_url = models.URLField(blank=False, null=False)

    submissions: models.Manager[ToolingChallengeSubmission] = models.Manager()

    def get_absolute_url(self) -> str:
        """Return a URL for viewing the submission status"""
        return reverse(SUMBISSION_VIEW, args=[self.uuid])
