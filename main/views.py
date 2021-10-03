from django.shortcuts import render
from .models import *
from asgiref.sync import sync_to_async
from django.contrib.auth.decorators import login_required
from .templatetags import extra
from django.conf import settings
from django.contrib import messages
from accounts.models import User
from .decorators import verify_entry_to_group


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
@verify_entry_to_group
def group_make(request):
    parameters = {
            'group': GameGroup.objects.filter(users__in=[request.user],solo_or_squad='sq').all(),
            'solo': GameGroup.objects.filter(users__in=[request.user],solo_or_squad='so').all(),
            'no_display_messages': True
        }
    if request.method == 'POST':
        group_id, users_list, inavlid_users_list = '', [], []
        for i in request.POST.dict():
            if 'userid' in i:
                tuple_3 = i.split(' ')
                group_id = tuple_3[1]
                if User.objects.filter(unique_id=request.POST.dict()[i]).exists():
                    users_list.append(User.objects.filter(unique_id=request.POST.dict()[i]))
                else:
                    inavlid_users_list.append(request.POST.dict()[i])
        if len(users_list) > 0:
            groups=GameGroup.objects.filter(group_unique_id=group_id).get()     
            groups.save()
            for i in users_list:
                groups.users.add(i[0].id)
            messages.success(request, f'Successfully added {len(users_list)} user(s) to the group!')
            parameters.update({'message_group_id': group_id})
        if len(inavlid_users_list) > 0:
            messages.error(request, f'Unable to add {len(users_list)} user(s) to the group!')
            messages.error(request, 'Make sure that they have registered themselves first ¯\_(ツ)_/¯')
            parameters.update({'message_group_id': group_id})
        try:
            groups.group_name = request.POST.get('groupname')
            groups.save()
            messages.success(request, f'Successfully updated Group Name')
        except:
            messages.error(request, 'This is already taken please try some other group name ¯\_(ツ)_/¯')
    print(parameters)        
    return render(
        request,
        'groups.html',
        parameters
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
