"""Tests for mentor_certs forms"""
import pytest
from django.http import QueryDict

from ..forms import MailJobForm
from ..models import Course, MailJob


@pytest.mark.django_db
def test_mail_job_form_saves_job_with_course():
    """Test that the course given to the form is linked with the created mail
    job"""
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

    mj_query = MailJob.mail_jobs.filter(
        course=course, message_title=message_title, message_body=message_body
    )

    form = MailJobForm(post_data, course=course)

    # Ensure we don't have the appropriate object in the DB before saving
    assert not mj_query.exists()

    form.save()

    assert mj_query.exists()
    mail_job = mj_query.get()
    assert list(mail_job.certificates.values_list("pk", flat=True)) == [
        cert1.pk,
        cert2.pk,
    ]


@pytest.mark.django_db
def test_mail_job_form_make_sure_certificates_are_selected():
    """Test that the form validation fails if no certificates are selected"""
    course = Course.courses.get(name="Beyond OS 06")

    post_data = QueryDict(
        "&".join(
            (
                "message_title=some message title",
                "message_body=some message body text",
            )
        )
    )
    form = MailJobForm(post_data, course=course)

    assert not form.is_valid()
    assert list(form.errors) == ["certificates"]
