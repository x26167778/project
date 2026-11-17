from django.contrib import admin

from .models import LeaveRequest, LeaveType


@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        "employee",
        "leave_type",
        "start_date",
        "end_date",
        "status",
        "created_at",
    )
    list_filter = ("status", "leave_type", "start_date")
    search_fields = ("employee__username", "reason")
    readonly_fields = ("created_at",)
    date_hierarchy = "start_date"