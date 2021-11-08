import datetime
import uuid
from functools import lru_cache

from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from instamojo_wrapper import Instamojo

from main.models import GameGroup, Games

from .decorators import verify_entry_for_orders, verify_entry_for_payments_history
from .models import ComboOffers, Payments
from .templatetags import payments_extras


@sync_to_async
@login_required
@verify_entry_for_payments_history
def view_payments_history(request):
    return render(
        request,
        "payments.html",
        {"payments": request.user.orders.all(), "title": "Payments History"},
    )


@lru_cache(maxsize=5)
@sync_to_async
@login_required
@verify_entry_for_orders
def make_order(request):
    if request.method == "POST":
        # calculating orders amount logic
        order_list, total_value, undiscounted_value = [], 0, False
        for i in request.POST.dict():
            if "mode" in i:
                a = request.POST.dict()[i]
                gamename = (
                    a.replace("SelectGame", "")
                    .replace("SingleGame", "")
                    .replace("SquadGame", "")
                    .strip(" ")
                )
                if "SelectGame" in a:
                    mode, make_req = "SelectGame", False
                elif "SingleGame" in a:
                    mode, make_req, filter_name = "so", True, "solo_entry"
                else:
                    mode, make_req, filter_name = "sq", True, "squad_entry"
                if make_req:
                    order_value = (
                        Games.objects.filter(game_unique_id=gamename)
                        .values(filter_name)
                        .get()[filter_name]
                    )
                    total_value += order_value
                    order_list.append([gamename, mode, order_value])
        squad_list = [i[1] for i in order_list]
        applied_internal_discount = False
        if (
            "sq" in squad_list
            and "so" not in squad_list
            and settings.ALL_SQUAD_PRICE is not None
            and Games.objects.filter(has_squad_entry=True).count()
            == squad_list.count("sq")
        ):
            total_value = int(settings.ALL_SQUAD_PRICE)
            applied_internal_discount = True
        elif (
            "sq" not in squad_list
            and "so" in squad_list
            and settings.ALL_SOLO_PRICE is not None
            and Games.objects.filter(has_solo_entry=True).count()
            == squad_list.count("so")
        ):
            total_value = int(settings.ALL_SOLO_PRICE)
            applied_internal_discount = True
        else:
            if not ComboOffers.objects.count() <= 0:
                games_list = [i[0] for i in order_list]
                for i in ComboOffers.objects.iterator():
                    combo_offers_games_list = [
                        j.game_unique_id.lower() for j in i.games.iterator()
                    ]
                    users_selected_games_list = []
                    squad_list = []
                    for j in games_list:
                        if j.lower() in combo_offers_games_list:
                            users_selected_games_list.append(j.lower())
                    if combo_offers_games_list == users_selected_games_list:
                        for j in order_list:
                            if j[0].lower() in users_selected_games_list:
                                squad_list.append(j[1])
                        if squad_list.count(squad_list[0]) == len(squad_list) and (
                            squad_list[0] == "sq"
                            and i.if_squad
                            or squad_list[0] == "so"
                            and i.if_solo
                        ):
                            for j in order_list:
                                if j[0].lower() in users_selected_games_list:
                                    total_value -= int(j[-1])
                            if squad_list[0] == "sq":
                                total_value += int(i.squad)
                            else:
                                total_value += int(i.solo)
                applied_internal_discount = True
        # discount code logic
        if request.user.referral_code:
            discount_value = request.user.referral_code.discount_percentage
            undiscounted_value = int(total_value)
            total_value = total_value * (1 - (discount_value / 100))
        if total_value > 0:
            request.session["order_list"] = order_list
            request.session["total_value"] = total_value
            return render(
                request,
                "checkout.html",
                {
                    "total_value": total_value,
                    "action_url": reverse("create_payment"),
                    "title": "Pay for the Games that you want to participate",
                    "undiscounted_value": undiscounted_value,
                    "applied_internal_discount": applied_internal_discount,
                },
            )
        messages.error(request, "Please select something in order to pay!")
    return render(
        request,
        "checkout.html",
        {
            "games": Games.objects.all(),
            "payafter": False,
            "display_games": True,
            "title": "Pay for the Games that you want to participate",
        },
    )


@sync_to_async
@login_required
@verify_entry_for_orders
def create_payment(request):
    if request:
        messages.info(request, "Please read this announcement message!")
        return HttpResponsePermanentRedirect('/announcements/23b3bce7-c7cb-45a9-9947-2af628791902')
    amount = str(request.session.get("total_value"))
    purpose = str(uuid.uuid4())
    buyers_name = f"{request.user.first_name} {request.user.last_name}"
    email = request.user.email
    phone = request.user.phone

    current_site = get_current_site(request)
    redirect_url = f'{request.scheme}://{current_site.domain}{reverse("payment_stats")}'

    allow_repeated_payments = False
    send_email = True
    send_sms = True
    if settings.LOCAL:
        api = Instamojo(
            api_key=settings.INSTAMOJO_AUTH_KEY,
            auth_token=settings.INSTAMOJO_PRIVATE_TOKEN,
            endpoint="https://test.instamojo.com/api/1.1/",
        )
    else:
        api = Instamojo(
            api_key=settings.INSTAMOJO_AUTH_KEY,
            auth_token=settings.INSTAMOJO_PRIVATE_TOKEN,
        )

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
    pay = Payments(
        order_id=purpose,
        request_id_instamojo=response.get("payment_request")["id"],
        amount=int(request.session["total_value"]),
        payment_status="P",
        orders_list=str(request.session["order_list"]),
    )
    pay.save()
    request.user.orders.add(pay)
    return HttpResponsePermanentRedirect(response.get("payment_request")["longurl"])


@sync_to_async
@login_required
@verify_entry_for_payments_history
def payment_stats(request):
    payment_id = request.GET["payment_id"]
    payment_request_id = request.GET["payment_request_id"]
    payment_status = request.GET["payment_status"]
    if "credit" in payment_status.lower():
        try:
            payment_obj = Payments.objects.filter(
                request_id_instamojo=payment_request_id
            ).get()
            payment_obj.payment_status = "S"
            payment_obj.instamojo_order_id = payment_id
            payment_obj.save()
            messages.success(
                request, "You have successfully paid the amount! Please wait for 2secs"
            )

            order_list = request.session.get("order_list")

            for i in order_list:
                game = Games.objects.filter(game_unique_id=i[0]).get()
                game_group = GameGroup(
                    game=game, payment_id=payment_obj, solo_or_squad=i[1]
                )
                game_group.save()
                game_group.users.add(request.user)

            redirect_link = reverse("make_groups")
        except Payments.DoesNotExist:
            messages.error(request, "The transaction does not exists")
            redirect_link = reverse("make_order")
        except:
            messages.error(
                request,
                "There was some error processing at the backend! Please contact the support",
            )
            redirect_link = reverse("make_order")
    else:
        messages.error(request, "The payment failed")
        redirect_link = reverse("make_order")
    try:
        del request.session["order_list"]
    except:
        pass
    try:
        del request.session["total_value"]
    except:
        pass
    return render(
        request,
        "checkout.html",
        {
            "payafter": True,
            "redirect_link": redirect_link,
            "title": "Payment Status check or verifier",
        },
    )


@sync_to_async
@csrf_exempt
@require_POST
def update_payments(request):
    try:
        payments = Payments.objects.filter(payment_status="P").iterator()
        for i in payments:
            if i.created_at <= now() - datetime.timedelta(minutes=10):
                i.payment_status = "F"
                i.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": e})
