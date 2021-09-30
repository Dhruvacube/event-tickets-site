from django.shortcuts import render
from .models import *
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required

@sync_to_async
def home(request):
    return render(
        request,
        'index.html',
        {
            'games': Games.objects.all()
        }
    )

@sync_to_async
@login_required
def group_make(request):
    return render(
        request,
        'groups.html',
        {
            'group': GameGroup.objects.filter(users__in=[request.user],solo_or_squad='sq').all(),
            'solo': GameGroup.objects.filter(users__in=[request.user],solo_or_squad='so').all()
        }
    )

@sync_to_async
def view_games(request, game_id: int):
    return render(
        request,
        'about_games.html',
        {
            'game': Games.object.filter(id=game_id).get()
        }
    )
