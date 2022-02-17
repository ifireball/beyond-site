"""Test data for mentor_certs"""
# pylint: disable=invalid-name, import-outside-toplevel, too-many-locals, unused-argument
# pylint: disable=no-self-argument, no-self-use
from django.db import migrations, transaction


class Migration(migrations.Migration):
    """Migration for creating test data"""

    dependencies = [
        ("mentor_certs", "0001_initial"),
    ]

    def generate_data(apps, schema_editor):
        """Creates the test data"""
        from django.conf import settings

        if not settings.DEBUG:
            return

        from datetime import date

        from django.db import models

        from mentor_certs.models import Certificate, Course, StaffMember

        with transaction.atomic():
            course_and_instructors = (
                beyond_os07 := Course(
                    name="Beyond OS 06",
                    start_date=date(2021, 10, 10),
                    end_date=date(2022, 1, 2),
                ),
                beyond_cy01 := Course(
                    name="Beyond Cyber 01",
                    start_date=date(2021, 10, 17),
                    end_date=date(2022, 12, 26),
                ),
                bkorren := StaffMember(name="Barak Korren", email="bkorren@redhat.com"),
                khakimi := StaffMember(name="Kobi Hakimi", email="bkorren@redhat.com"),
                oamsalem := StaffMember(
                    name="Omer Amsalem", email="bkorren@redhat.com"
                ),
                hkrasnik := StaffMember(
                    name="Haim Krasniker", email="bkorren@redhat.com"
                ),
                lnachshon := StaffMember(
                    name="Luiza Nachshon", email="bkorren@redhat.com"
                ),
            )
            obj: models.Model
            for obj in course_and_instructors:
                obj.save()

            Certificate(
                course=beyond_os07,
                staff_member=bkorren,
                mentor_level=Certificate.MentorLevel.MENTOR_LEAD4,
                instructor_level=Certificate.InstructorLevel.COURSE_LEAD,
            ).save()
            Certificate(
                course=beyond_os07,
                staff_member=khakimi,
                mentor_level=Certificate.MentorLevel.MENTOR_LEAD1,
                instructor_level=Certificate.InstructorLevel.SPEAKER,
            ).save()
            Certificate(
                course=beyond_os07,
                staff_member=oamsalem,
                mentor_level=Certificate.MentorLevel.MENTOR4,
            ).save()
            Certificate(
                course=beyond_cy01,
                staff_member=hkrasnik,
                mentor_level=Certificate.MentorLevel.NONE,
                instructor_level=Certificate.InstructorLevel.COURSE_LEAD,
            ).save()
            Certificate(
                course=beyond_cy01,
                staff_member=lnachshon,
                mentor_level=Certificate.MentorLevel.MENTOR1,
                instructor_level=Certificate.InstructorLevel.SPEAKER,
            ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
