"""Forms for mentor_certs"""
from django import forms

from .models import Course, MailJob


class MailJobForm(forms.ModelForm):
    """Form for ceariting MailJob objects"""

    _course: Course

    class Meta:
        model = MailJob
        fields = ["message_title", "message_body", "certificates"]
        widgets = {"certificates": forms.CheckboxSelectMultiple}
        error_messages = {
            "certificates": {
                "required": "Please select at least one certificate to send"
            },
        }

    def __init__(self, *args: object, course: Course, **kwargs: object):
        super().__init__(*args, **kwargs)
        self.fields["certificates"].queryset = course.certificate_set
        self._course = course

    def save(self, commit=True):
        """Save the MailJob object while filling-in the course field"""
        new_mail_job = super().save(commit=False)
        new_mail_job.course = self._course
        if commit:
            new_mail_job.save()
            self.save_m2m()
        return new_mail_job
