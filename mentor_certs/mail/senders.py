"""mentor_certs.mail.senders - things that can actually send mail"""
from dataclasses import dataclass

from django.core.mail.backends import dummy
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import EmailMessage

from ..models import Certificate, MailJob
from .protocols import CertificateMailSender, MailJobRunner


@dataclass(frozen=True)
class MailJobSender(MailJobRunner):
    """Use a CertificateMailSender to handle a MailJob"""

    send_certificate: CertificateMailSender = lambda mail_job, certificate: None

    def __call__(self, mail_job: MailJob) -> None:
        """Send the certificates linked to the given MailJob"""
        for certificate in mail_job.certificates.all():
            self.send_certificate(mail_job, certificate)


@dataclass(frozen=True)
class CertificateMailer(CertificateMailSender):
    """Sends a certificate via the given mail backend"""

    email_backend: BaseEmailBackend = dummy.EmailBackend()

    def __call__(self, mail_job: MailJob, certificate: Certificate) -> None:
        """Send the provided certificate via email"""
        message = EmailMessage(
            connection=self.email_backend,
            to=(certificate.staff_member.email,),
            subject=mail_job.message_title,
            body=mail_job.message_body,
        )
        message.send(fail_silently=False)
