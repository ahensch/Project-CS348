from django.shortcuts import render
from django.db.models import Sum
from .models import Member, Event, HourLog, SemesterRequirement


def home(request):
    return render(request, "tracker/home.html")


def hours_report(request):
    # Dropdown choices
    members = Member.objects.all()

    # Selected filter
    selected_member = request.GET.get("member")

    # If a member is selected, filter to only that member
    if selected_member:
        filtered_members = members.filter(id=selected_member)
    else:
        filtered_members = members

    report_data = []

    # Get requirements (we assume only one semester requirement for demo)
    req = SemesterRequirement.objects.first()

    for member in filtered_members:
        logs = HourLog.objects.filter(member=member)

        # Calculate hours by category
        service_hours = logs.filter(event__category="Service").aggregate(Sum("hours"))["hours__sum"] or 0
        comm_hours = logs.filter(event__category="Communication").aggregate(Sum("hours"))["hours__sum"] or 0
        mem_hours = logs.filter(event__category="Membership").aggregate(Sum("hours"))["hours__sum"] or 0
        finance_hours = logs.filter(event__category="Finance").aggregate(Sum("hours"))["hours__sum"] or 0
        ld_hours = logs.filter(event__category="Leadership").aggregate(Sum("hours"))["hours__sum"] or 0
        chimps = logs.filter(event__category="CHIMPS").count()

        total_completed = (
            service_hours + comm_hours + mem_hours + finance_hours + ld_hours
        )

        # If requirements exist, compare
        if req:
            rows = [
                ("Service Hours", service_hours, req.service_hours_required),
                ("Communication Hours", comm_hours, req.comm_hours_required),
                ("Membership Hours", mem_hours, req.membership_hours_required),
                ("Finance Hours", finance_hours, req.finance_hours_required),
                ("Leadership Development", ld_hours, req.ld_hours_required),
                ("CHIMPS", chimps, req.chimps_required),
            ]

            total_required = (
                req.service_hours_required +
                req.comm_hours_required +
                req.membership_hours_required +
                req.finance_hours_required +
                req.ld_hours_required
            )
        else:
            rows = []
            total_required = 0

        report_data.append({
            "member": member,
            "rows": rows,
            "total_completed": total_completed,
            "total_required": total_required,
            "met": total_completed >= total_required,
        })

    return render(request, "tracker/hours_report.html", {
        "members": members,
        "report_data": report_data,
        "selected_member": selected_member,
    })
