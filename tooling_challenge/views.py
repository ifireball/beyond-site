"""tooling_challenge views"""
from uuid import UUID

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from .forms import SubmissionForm


def submission_form(request: HttpRequest) -> HttpResponse:
    """Process the request submission form"""
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            return redirect(submission)
    else:
        form = SubmissionForm()
    return TemplateResponse(
        request,
        "tooling_challenge/submission_form.html",
        context={"form": form},
    )


def submission_status(request: HttpRequest, *, submission_uuid: UUID) -> HttpResponse:
    """Show the status for an existing requiest"""
    assert submission_uuid  # appease pylint for now
    return TemplateResponse(request, "tooling_challenge/submission_status.html")
