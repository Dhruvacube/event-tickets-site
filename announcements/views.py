from asgiref.sync import sync_to_async
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from main.models import GameGroup

from .models import *


@sync_to_async
@login_required
def view_annoucements(request):
    groups = list(
        GameGroup.objects.filter(users__in=[
            request.user,
        ]).iterator())
    announcements = (GlobalAnnouncements.objects.filter(publish=True).union(
        GroupsAnnouncements.objects.filter(
            groups__in=groups, publish=True).union(
                UsersAnnouncements.objects.filter(
                    users__in=[
                        request.user,
                    ],
                    publish=True,
                ))).reverse())

    if announcements.count() <= 0:
        messages.info(request, r"No announcements there ¯\_(ツ)_/¯")
        return redirect(reverse("home"))

    page = request.GET.get("page", 1)
    paginator = Paginator(
        announcements.order_by("announncement_creation_date"), 4)

    try:
        announcements = paginator.page(page)
    except PageNotAnInteger:
        announcements = paginator.page(1)
    except EmptyPage:
        announcements = paginator.page(paginator.num_pages)

    return render(
        request,
        "all_announcements.html",
        {
            "announcements": announcements,
            "title": "Announcements"
        },
    )


@sync_to_async
@login_required
def view_annoucements_full(request, announcement_id):
    all_ = GlobalAnnouncements.objects.filter(
        announcement_id__in=[
            announcement_id,
        ],
        publish=True,
    )
    groups = GroupsAnnouncements.objects.filter(
        announcement_id__in=[
            announcement_id,
        ],
        publish=True,
    )
    users = UsersAnnouncements.objects.filter(
        announcement_id__in=[
            announcement_id,
        ],
        publish=True,
    )
    if all_.union(groups.union(users)).count() <= 0:
        raise Http404("No annoucement with that ID :)")

    return render(
        request,
        "announcements_details.html",
        {
            "announcement": all_.union(groups.union(users))[0],
            "title": f"Announcements Deatils | {announcement_id}",
        },
    )
