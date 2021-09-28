from django.shortcuts import render
from .models import *
from asgiref.sync import sync_to_async

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
def group_make(request):
    return render(
        request,
        'groups.html',
        {
            'games': Games.objects.all()
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
