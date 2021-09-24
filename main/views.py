from django.shortcuts import render
from .models import *

# Create your views here.
def main(request):
    return render(
        request,
        'index.html',
        {
            'games': Games.objects.all()
        }
    )

def view_games(request, game_id: int):
    return render(
        request,
        'about_games.html',
        {
            'game': Games.object.filter(id=game_id).get()
        }
    )
