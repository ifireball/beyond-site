"""
Tests for mentor_certs app views
"""
from random import choice
from unittest.mock import call, create_autospec

import pytest
from django.http import QueryDict
from django.test import Client, RequestFactory

from mentor_certs.mail.protocols import MailJobRunner
from mentor_certs.models import Certificate, Course, MailJob
from mentor_certs.views import MailView


@pytest.mark.django_db
def test_default_redircet(client: Client) -> None:
    """Test the the app root redirects to the default certificate"""
    default_cert = Certificate.certificates.default
    expected_path = f"/mentor_certs/certificate/{default_cert.pk}"

    response = client.get("/mentor_certs/")

    assert response.status_code == 302
    assert response.url == expected_path


@pytest.mark.django_db
def test_certificate_view(client: Client) -> None:
    """Test that the certificate view displays the asked-for certificate"""
    some_cert = choice(Certificate.certificates.all())

    response = client.get(f"/mentor_certs/certificate/{some_cert.pk}")

    assert response.status_code == 200
    template_names = [tmpl.origin.template_name for tmpl in response.templates[0:1]]
    assert template_names == ["mentor_certs/certificate_view.html"]
    shown_cert = response.context["certificate"]
    assert shown_cert == some_cert


@pytest.mark.django_db
def test_mail_view_sends_mail(rf: RequestFactory) -> None:
    """Test that the MailView sends out emails when the form is posted"""
    course = Course.courses.get(name="Beyond OS 06")
    course_certes = course.certificate_set.all()
    cert1 = course_certes[0]
    cert2 = course_certes[1]

    message_title = "some message title"
    message_body = "some message body text"
    post_data = QueryDict(
        "&".join(
            map(
                "=".join,
                (
                    ("message_title", message_title),
                    ("message_body", message_body),
                    ("certificates", str(cert1.pk)),
                    ("certificates", str(cert2.pk)),
                ),
            )
        )
    )
    post_request = rf.post("/some/path", post_data)
    mj_query = MailJob.mail_jobs.filter(
        course=course, message_title=message_title, message_body=message_body
    )
    mail_job_runner = create_autospec(MailJobRunner)
    mail_view = MailView(mail_job_runner)

    # Ensure we don't have the appropriate object in the DB before posting
    assert not mj_query.exists()

    mail_view(post_request, course_id=course.pk)

    assert mj_query.exists()
    mail_job = mj_query.get()
    assert mail_job_runner.call_args_list == [call(mail_job)]
