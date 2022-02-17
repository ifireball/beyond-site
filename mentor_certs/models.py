"""mentor_certs models"""
from django.db import models


class StaffMember(models.Model):
    """Information about Beyond staff members"""

    name = models.CharField(blank=False, null=False, max_length=200)
    email = models.EmailField(blank=False, null=False)

    def __str__(self):
        return self.name


class Course(models.Model):
    """Information about Beyond courses"""

    name = models.CharField(unique=True, blank=False, null=False, max_length=60)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    staff = models.ManyToManyField(to=StaffMember, through="Certificate")

    def __str__(self):
        return self.name


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
