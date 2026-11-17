from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import LeaveRequestForm
from .models import LeaveRequest

# Managers are identified by the permission we gave the Manager group.
manager_required = permission_required("leaves.change_leaverequest", raise_exception=True)


@login_required
def home(request):
    """Send each user to the right landing page for their role."""
    if request.user.has_perm("leaves.change_leaverequest"):
        return redirect("manager_dashboard")
    return redirect("my_leave_list")


# ---------- Employee views ----------

@login_required
def my_leave_list(request):
    leaves = LeaveRequest.objects.filter(employee=request.user)
    return render(request, "leaves/my_leave_list.html", {"leaves": leaves})


@login_required
def leave_create(request):
    if request.method == "POST":
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user
            leave.save()
            messages.success(request, "Leave request submitted.")
            return redirect("my_leave_list")
    else:
        form = LeaveRequestForm()
    return render(request, "leaves/leave_form.html", {"form": form, "title": "Apply for leave"})


@login_required
def leave_edit(request, pk):
    leave = get_object_or_404(
        LeaveRequest,
        pk=pk,
        employee=request.user,
        status=LeaveRequest.Status.PENDING,
    )
    if request.method == "POST":
        form = LeaveRequestForm(request.POST, instance=leave)
        if form.is_valid():
            form.save()
            messages.success(request, "Leave request updated.")
            return redirect("my_leave_list")
    else:
        form = LeaveRequestForm(instance=leave)
    return render(request, "leaves/leave_form.html", {"form": form, "title": "Edit leave request"})


@login_required
@require_POST
def leave_cancel(request, pk):
    leave = get_object_or_404(
        LeaveRequest,
        pk=pk,
        employee=request.user,
        status=LeaveRequest.Status.PENDING,
    )
    leave.status = LeaveRequest.Status.CANCELLED
    leave.save()
    messages.success(request, "Leave request cancelled.")
    return redirect("my_leave_list")


# ---------- Manager views ----------

@login_required
@manager_required
def manager_dashboard(request):
    # Managers never see (or act on) their own requests here.
    others = LeaveRequest.objects.select_related("employee", "leave_type").exclude(
        employee=request.user
    )
    pending = others.filter(status=LeaveRequest.Status.PENDING).order_by("start_date")
    decided = others.filter(
        status__in=[LeaveRequest.Status.APPROVED, LeaveRequest.Status.REJECTED]
    )[:10]
    return render(
        request,
        "leaves/manager_dashboard.html",
        {"pending": pending, "decided": decided},
    )


@login_required
@manager_required
@require_POST
def leave_decide(request, pk, decision):
    new_status = {
        "approve": LeaveRequest.Status.APPROVED,
        "reject": LeaveRequest.Status.REJECTED,
    }.get(decision)
    if new_status is None:
        raise Http404

    # Only pending requests, and never the manager's own request.
    leave = get_object_or_404(
        LeaveRequest.objects.exclude(employee=request.user),
        pk=pk,
        status=LeaveRequest.Status.PENDING,
    )
    leave.status = new_status
    leave.save()
    messages.success(
        request, f"Leave request for {leave.employee} has been {leave.get_status_display().lower()}."
    )
    return redirect("manager_dashboard")