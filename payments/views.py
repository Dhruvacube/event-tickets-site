from django.shortcuts import render
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.views.decorators.http import require_GET, require_POST
from asgiref.sync import sync_to_async

import uuid

import datetime
from instamojo_wrapper import Instamojo
from main.models import Games, GameGroup
from .models import Payments
from .templatetags import payments_extras
from .decorators import verify_entry_for_orders, verify_entry_for_payments_history


@sync_to_async
@login_required
@verify_entry_for_payments_history
def view_payments_history(request):
    return render(
        request,
        'payments.html',
        {
            'payments': request.user.orders.all(),
            'title': 'Payments History'
        }
    )


@sync_to_async
@login_required
@verify_entry_for_orders
def make_order(request):
    if request.method == 'POST':
        order_list, total_value = [], 0
        for i in request.POST.dict():
            if 'mode' in i:
                a = request.POST.dict()[i]
                gamename = a.replace('SelectGame', '').replace(
                    'SingleGame', '').replace('SquadGame', '').strip(' ')
                if 'SelectGame' in a:
                    mode, make_req = 'SelectGame', False
                elif 'SingleGame' in a:
                    mode, make_req, filter_name = 'so', True, 'solo_entry'
                else:
                    mode, make_req, filter_name = 'sq', True, 'squad_entry'
                if make_req:
                    order_value = Games.objects.filter(
                        name=gamename).values(filter_name).get()[filter_name]
                    total_value += order_value
                    order_list.append([gamename, mode, order_value])
        if not total_value <= 0:
            request.session['order_list'] = order_list
            request.session['total_value'] = total_value
            return render(
                request,
                'checkout.html',
                {
                    'total_value': total_value,
                    'action_url': reverse('create_payment'),
                    'title': 'Pay for the Games that you want to participate',
                }
            )
        else:
            messages.error(request, "Please select something in order to pay!")
    return render(
        request,
        'checkout.html',
        {
            'games': Games.objects.all(),
            'payafter': False,
            'display_games': True,
            'title': 'Pay for the Games that you want to participate'
        }

    )


@sync_to_async
@login_required
@verify_entry_for_orders
def create_payment(request):
    amount = str(request.session.get('total_value'))
    purpose = str(uuid.uuid4())
    buyers_name = f"{request.user.first_name} {request.user.last_name}"
    email = request.user.email
    phone = request.user.phone

    current_site = get_current_site(request)
    redirect_url = f'{request.scheme}://{current_site.domain}{reverse("payment_stats")}'

    allow_repeated_payments = False
    send_email = True
    send_sms = True
    expires_at = datetime.datetime.now() + datetime.timedelta(days=0, seconds=600)

    if settings.LOCAL:
        api = Instamojo(api_key=settings.INSTAMOJO_AUTH_KEY, auth_token=settings.INSTAMOJO_PRIVATE_TOKEN,
                        endpoint='https://test.instamojo.com/api/1.1/')
    else:
        api = Instamojo(api_key=settings.INSTAMOJO_AUTH_KEY,
                        auth_token=settings.INSTAMOJO_PRIVATE_TOKEN)

    # Create a new Payment Request
    response = api.payment_request_create(
        amount=amount,
        purpose=purpose,
        buyer_name=buyers_name,
        email=email,
        phone=phone,

        redirect_url=redirect_url,
        allow_repeated_payments=allow_repeated_payments,
        send_email=send_email,
        send_sms=send_sms,
    )
    pay = Payments(order_id=purpose, request_id_instamojo=response.get("payment_request")["id"], amount=int(
        request.session['total_value']), payment_status='P', orders_list=str(request.session['order_list']))
    pay.save()
    request.user.orders.add(pay)
    return HttpResponsePermanentRedirect(response.get("payment_request")["longurl"])


@sync_to_async
@login_required
@verify_entry_for_payments_history
def payment_stats(request):
    payment_id = request.GET['payment_id']
    payment_request_id = request.GET['payment_request_id']
    payment_status = request.GET['payment_status']
    if 'credit' in payment_status.lower():
        try:
            payment_obj = Payments.objects.filter(
                request_id_instamojo=payment_request_id).get()
            payment_obj.payment_status = 'S'
            payment_obj.instamojo_order_id = payment_id
            payment_obj.save()
            messages.success(
                request, 'You have successfully paid the amount! Please wait for 2secs')

            order_list = request.session.get('order_list')

            for i in order_list:
                game = Games.objects.filter(name=i[0]).get()
                game_group = GameGroup(
                    game=game, payment_id=payment_obj, solo_or_squad=i[1])
                game_group.save()
                game_group.users.add(request.user)

            redirect_link = reverse('make_groups')
        except Payments.DoesNotExist:
            messages.error(request, 'The transaction does not exists')
            redirect_link = reverse('make_order')
        except:
            messages.error(
                request, 'There was some error processing at the backend! Please contact the support')
            redirect_link = reverse('make_order')
    else:
        messages.error(request, 'The payment failed')
        redirect_link = reverse('make_order')
    try:
        del request.session['order_list']
    except:
        pass
    try:
        del request.session['total_value']
    except:
        pass
    return render(
        request,
        'checkout.html',
        {
            'payafter': True,
            'redirect_link': redirect_link,
            'title': 'Payment Status check or verifier'
        }
    )
