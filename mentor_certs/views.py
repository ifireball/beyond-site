"""mentor_certs views"""
from dataclasses import dataclass

from django.core.mail import get_connection
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from .forms import MailJobForm
from .mail.protocols import MailJobRunner
from .mail.senders import CertificateMailer, MailJobSender
from .models import Certificate, Course
from .render import pdf


def root(request: HttpRequest) -> HttpResponse:
    """The app root view - redirects to the default certificate"""
    return redirect(Certificate.certificates.default)


def certificate_view(request: HttpRequest, *, certificate_id: int) -> HttpResponse:
    """Display a certificate"""
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    return TemplateResponse(
        request, "mentor_certs/certificate_view.html", {"certificate": certificate}
    )


def certificate_pdf(request: HttpRequest, *, certificate_id: int) -> HttpResponse:
    """Retrive a certificate PDF file"""
    certificate = get_object_or_404(Certificate, pk=certificate_id)
    response = HttpResponse(
        pdf(certificate),
        headers={
            "Content-Type": "application/pdf",
            "Content-Disposition": f'attachment; filename="{certificate.pk}.pdf"',
        },
    )
    return response


@dataclass(frozen=True)
class MailView:
    """A mail-sending view"""

    mail_job_runner: MailJobRunner = lambda mjob: None

    def __call__(self, request: HttpRequest, *, course_id: int) -> HttpResponse:
        """Show the certificate mailing form"""
        course = get_object_or_404(Course, pk=course_id)
        if request.POST:
            form = MailJobForm(request.POST, course=course)
            if form.is_valid():
                mail_job = form.save()
                self.mail_job_runner(mail_job)
                return redirect(course.certificate_set.first())
        else:
            form = MailJobForm(course=course)
        return TemplateResponse(
            request, "mentor_certs/mail.html", {"course": course, "form": form}
        )


mail = MailView(MailJobSender(CertificateMailer(get_connection())))
