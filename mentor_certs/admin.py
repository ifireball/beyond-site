"""Django admin app configuration"""
from django.contrib import admin

from .models import Certificate, Course, MailJob, MailJobCertificateResult, StaffMember


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    """Admin class for StaffMember"""

    list_display = ("name", "email")
    list_editable = ("name", "email")
    list_display_links = None


class CertificateAdmin(admin.TabularInline):
    """Admin class for CertificateAdmin"""

    model = Certificate
    list_display = ("staff_member", "course", "mentor_level", "instructor_level")


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Admin class for Course"""

    list_display = ("name", "start_date", "end_date")
    inlines = [CertificateAdmin]


class MailJobCertificateResultAdmin(admin.TabularInline):
    """Admin class for MailJobCertificateResult"""

    model = MailJobCertificateResult
    list_display = ("certificate", "status", "log")


@admin.register(MailJob)
class MailJobAdmin(admin.ModelAdmin):
    """Admin class for MailJob"""

    model = MailJob
    inlines = [MailJobCertificateResultAdmin]
