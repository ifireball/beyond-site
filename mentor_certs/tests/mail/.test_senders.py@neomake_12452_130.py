"""Tests for mentor_certs.mail.senders"""
# pylint: disable=redefined-outer-name
from typing import Collection
from unittest.mock import call, create_autospec

import pytest

from mentor_certs.mail.protocols import CertificateMailSender
from mentor_certs.mail.senders import MailJobSender
from mentor_certs.models import Certificate, Course, MailJob


@pytest.fixture
def course() -> Course:
    """A Course fixture"""
    return Course.courses.get(name="Beyond OS 06")


@pytest.fixture
def course_certes(course: Course) -> Collection[Certificate]:
    """The set of certificates in the course"""
    return course.certificate_set.all()


@pytest.mark.django_db
def test_mail_job_sender_calls_certificate_senders() -> None:
    """The MailJobSender call a CertificateMailSender for each certificae in
    the MailJob"""

    course = Course.courses.get(name="Beyond OS 06")
    course_certes = course.certificate_set.all()
    cert1 = course_certes[0]
    cert2 = course_certes[1]

    mail_job = MailJob(
        course=course,
        message_title="some message title",
        message_body="some message body text",
    )
    mail_job.save()
    mail_job.certificates.add(cert1, cert2)

    send_certificate = create_autospec(CertificateMailSender)
    mail_job_sender = MailJobSender(send_certificate)

    mail_job_sender(mail_job)

    assert send_certificate.call_args_list == [
        call(mail_job, cert1),
        call(mail_job, cert2),
    ]


@pytest.mark.django_db
def test_certificate_mailer_sends_out_certificates() -> None:
    """The CertificateMailer class send out the certificates via the provided
    email backend"""
