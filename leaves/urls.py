from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("leaves/", views.my_leave_list, name="my_leave_list"),
    path("leaves/new/", views.leave_create, name="leave_create"),
    path("leaves/<int:pk>/edit/", views.leave_edit, name="leave_edit"),
    path("leaves/<int:pk>/cancel/", views.leave_cancel, name="leave_cancel"),
    path("manager/", views.manager_dashboard, name="manager_dashboard"),
    path("manager/leaves/<int:pk>/approve/", views.leave_decide, {"decision": "approve"}, name="leave_approve"),
    path("manager/leaves/<int:pk>/reject/", views.leave_decide, {"decision": "reject"}, name="leave_reject"),
]