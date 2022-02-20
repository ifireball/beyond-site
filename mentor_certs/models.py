"""mentor_certs models"""
from __future__ import annotations

from django.db import models


class StaffMember(models.Model):
    """Information about Beyond staff members"""

    name = models.CharField(blank=False, null=False, max_length=200)
    email = models.EmailField(blank=False, null=False)

    class Meta:
        ordering = ["name", "email"]

    def __str__(self):
        return self.name


class Course(models.Model):
    """Information about Beyond courses"""

    name = models.CharField(unique=True, blank=False, null=False, max_length=60)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    staff = models.ManyToManyField(to=StaffMember, through="Certificate")

    class Meta:
        ordering = ["-end_date"]

    def __str__(self):
        return self.name


class CertificatesManager(models.Manager["Certificate"]):
    """Model manager for certificates"""

    @property
    def default(self) -> Certificate:
        """Get the certificate from the most recently ended course for the
        first staff memebr when ordered lexicographically"""
        return self.first()


class Certificate(models.Model):
    """Participation certificates granted to course staff"""

    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    staff_member = models.ForeignKey(to=StaffMember, on_delete=models.CASCADE)

    class MentorLevel(models.IntegerChoices):
        """Mentoring badges"""

        NONE = 0, "Not a mentor"
        MENTOR1 = 1, "mentor (1 semester)"
        MENTOR2 = 2, "mentor (2 semesters)"
        MENTOR3 = 3, "mentor (3 semesters)"
        MENTOR4 = 4, "mentoring star! (4+ semesters)"
        MENTOR_LEAD1 = 101, "lead mentor (1 semester)"
        MENTOR_LEAD2 = 102, "lead mentor (2 semesters)"
        MENTOR_LEAD3 = 103, "lead mentor (3 semesters)"
        MENTOR_LEAD4 = 104, "leading star! (4+ semesters)"

    class InstructorLevel(models.IntegerChoices):
        """Intructor badges"""

        NONE = 0, "Not an instructor"
        SPEAKER = 100001, "Speaker"
        COURSE_LEAD = 100002, "Course lead"

    mentor_level = models.IntegerField(
        choices=MentorLevel.choices, default=MentorLevel.NONE
    )
    instructor_level = models.IntegerField(
        choices=InstructorLevel.choices, default=InstructorLevel.NONE
    )

    class Meta:
        ordering = ["course", "staff_member"]

    certificates = CertificatesManager()

    def __str__(self) -> str:
        return f"{self.staff_member.name} ({self.course.name})"

    @property
    def nav_previous(self) -> Certificate:
        """points to the previous certificate in the same course ordered
        lexicographically by staff_member name or None if its the first one"""
        return self.course.certificate_set.filter(
            staff_member__name__lt=self.staff_member.name
        ).last()

    @property
    def nav_next(self) -> Certificate:
        """points to the next certificate in the same course ordered
        lexicographically by staff_member name or None if its the last one"""
        return self.course.certificate_set.filter(
            staff_member__name__gt=self.staff_member.name
        ).first()

    @property
    def nav_courses(self) -> models.QuerySet[Certificate]:
        """Return a list of certificates that can be used to naviget to other
        courses"""
        return (
            self.__class__.certificates.exclude(course=self.course)
            .annotate(models.Min("course__staff__name"))
            .filter(staff_member__name=models.F("course__staff__name__min"))
        )
