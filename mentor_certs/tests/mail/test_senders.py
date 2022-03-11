"""Tests for mentor_certs.mail.senders"""
# pylint: disable=redefined-outer-name
from typing import Sequence
from unittest.mock import call, create_autospec

import pytest
from django.core.mail.backends import locmem
from django.core.mail.message import EmailMessage

from mentor_certs.mail.protocols import CertificateMailSender
from mentor_certs.mail.senders import CertificateMailer, MailJobSender
from mentor_certs.models import Certificate, Course, MailJob


@pytest.fixture
def course() -> Course:
    """A Course fixture"""
    return Course.courses.get(name="Beyond OS 06")


@pytest.fixture
def course_certes(course: Course) -> Sequence[Certificate]:
    """The set of certificates in the course"""
    return course.certificate_set.all()


@pytest.fixture
def cert1(course_certes: Sequence[Certificate]) -> Certificate:
    """The first certificate in the course"""
    return course_certes[0]


@pytest.fixture
def cert2(course_certes: Sequence[Certificate]) -> Certificate:
    """The 2nd certificate in the course"""
    return course_certes[1]


@pytest.fixture
def message_title() -> str:
    """The title for emails"""
    return "some message title"


@pytest.fixture
def message_body() -> str:
    """The body for emails"""
    return "some message body text"


@pytest.fixture
def mail_job(
    course: Course,
    cert1: Certificate,
    cert2: Certificate,
    message_title: str,
    message_body: str,
) -> MailJob:
    """A MailJob object for sending the two certificates"""
    the_mail_job = MailJob(
        course=course, message_title=message_title, message_body=message_body
    )
    the_mail_job.save()
    the_mail_job.certificates.add(cert1, cert2)
    return the_mail_job


@pytest.mark.django_db
def test_mail_job_sender_calls_certificate_senders(
    mail_job: MailJob, cert1: Certificate, cert2: Certificate
) -> None:
    """The MailJobSender call a CertificateMailSender for each certificae in
    the MailJob"""

    send_certificate = create_autospec(CertificateMailSender)
    mail_job_sender = MailJobSender(send_certificate)

    mail_job_sender(mail_job)

    assert send_certificate.call_args_list == [
        call(mail_job, cert1),
        call(mail_job, cert2),
    ]


@pytest.mark.django_db
def test_certificate_mailer_sends_out_certificates(
    mail_job: MailJob,
    cert1: Certificate,
    mailoutbox: Sequence[EmailMessage],
    message_title: str,
    message_body: str,
) -> None:
    """The CertificateMailer class send out the certificates via the provided
    email backend"""
    email_backend = locmem.EmailBackend()
    send_certificate = CertificateMailer(email_backend)

    send_certificate(mail_job, cert1)

    assert len(mailoutbox) == 1
    message = mailoutbox[0]
    assert message.recipients() == [cert1.staff_member.email]
    assert message.subject == message_title
    assert message.body == message_body
