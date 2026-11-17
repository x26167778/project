from django import forms
from django.utils import timezone

from .models import LeaveRequest


class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ["leave_type", "start_date", "end_date", "reason"]
        widgets = {
            "leave_type": forms.Select(attrs={"class": "form-select"}),
            "start_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date", "class": "form-control"}
            ),
            "reason": forms.Textarea(
                attrs={"rows": 4, "maxlength": 500, "class": "form-control"}
            ),
        }

    def clean_start_date(self):
        start_date = self.cleaned_data["start_date"]
        if start_date < timezone.localdate():
            raise forms.ValidationError("Start date cannot be in the past.")
        return start_date

    def clean_reason(self):
        reason = self.cleaned_data["reason"].strip()
        if len(reason) < 5:
            raise forms.ValidationError("Please provide a reason (at least 5 characters).")
        if len(reason) > 500:
            raise forms.ValidationError("Reason cannot exceed 500 characters.")
        return reason