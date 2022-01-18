import random
from functools import lru_cache

from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_page

from accounts.models import User

from .decorators import verify_entry_to_group
from .models import *
from .templatetags import extra


@sync_to_async
@cache_page(60 * 15)
def home(request):
    sponser = list(Sponser.objects.iterator())
    random.shuffle(sponser)
    return render(
        request,
        "index.html",
        {
            "games": Games.objects.all(),
            "title": "Home",
            "sponsers": sponser,
        },
    )


@sync_to_async
@login_required
@verify_entry_to_group
def group_make(request):
    parameters = {
        "title": "Register Groups",
    }
    if request.method == "POST":
        group_id, users_list = "", []
        for i in request.POST.dict():
            try:
                if "userid" in i:
                    tuple_3 = i.split(" ")
                    group_id = tuple_3[1]
                    group = GameGroup.objects.filter(
                        group_unique_id=group_id).get()
                    group.save()
                    group.users.clear()
                    group.users.add(request.user)
                    if (not request.POST.dict()[i].isspace()
                            or request.POST.dict()[i] != ""
                            or not request.POST.dict()[i]):
                        try:
                            user_object = User.objects.filter(
                                unique_id=request.POST.dict()[i])
                            if user_object.exists():
                                users_list.append(user_object)
                        except:
                            pass
            except Exception as e:
                messages.error(request, e)
                return redirect(reverse("make_groups"))
        if len(users_list) > 0:
            groups = GameGroup.objects.filter(group_unique_id=group_id).get()
            groups.save()
            for i in users_list:
                groups.users.add(i[0].id)
            messages.success(request, "Saved Successfully!")
            parameters.update({"message_group_id": group_id})
        try:
            groups.group_name = request.POST.get("groupname")
            groups.save()
        except Exception as e:
            messages.error(
                request,
                r"This is name already taken please try some other group name ¯\_(ツ)_/¯",
            )
        return redirect(reverse("make_groups"))
    parameters.update({
        "game_groups":
        list(GameGroup.objects.filter(users__in=[request.user]).iterator())
    })
    return render(request, "groups.html", parameters)


@sync_to_async
@cache_page(60 * 15)
def view_games(request, game_id: int):
    games = Games.objects.filter(id=game_id).get()
    return render(
        request,
        "about_games.html",
        {
            "game": games,
            "title": games.name,
        },
    )
