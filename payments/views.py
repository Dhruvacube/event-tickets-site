import ast
import datetime
import uuid

import razorpay
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponsePermanentRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from post_office import mail
from post_office.models import EmailTemplate

from main.models import GameGroup, Games
from main.tasks import mail_queue

from .decorators import verify_entry_for_orders, verify_entry_for_payments_history
from .models import ComboOffers, Payments
from .templatetags import payments_extras

razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,
                                        settings.RAZOR_KEY_SECRET))


@sync_to_async
@login_required
@verify_entry_for_payments_history
@cache_page(60 * 15)
def view_payments_history(request):
    return render(
        request,
        "payments.html",
        {
            "payments": request.user.orders.all(),
            "title": "Payments History"
        },
    )


@sync_to_async
@login_required
@verify_entry_for_orders
@cache_page(60 * 15)
def make_order(request):
    if request.method == "POST":
        # calculating orders amount logic
        order_list, total_value, undiscounted_value = [], 0, False
        for i in request.POST.dict():
            if "mode" in i:
                a = request.POST.dict()[i]
                gamename = (a.replace("SelectGame",
                                      "").replace("SingleGame",
                                                  "").replace("SquadGame",
                                                              "").strip(" "))
                if "SelectGame" in a:
                    mode, make_req = "SelectGame", False
                elif "SingleGame" in a:
                    mode, make_req, filter_name = "so", True, "solo_entry"
                else:
                    mode, make_req, filter_name = "sq", True, "squad_entry"
                if make_req:
                    order_value = (Games.objects.filter(
                        game_unique_id=gamename).values(filter_name).get()
                        [filter_name])
                    total_value += order_value
                    order_list.append([gamename, mode, order_value])
        squad_list = [i[1] for i in order_list]
        applied_internal_discount = False
        if ("sq" in squad_list and "so" not in squad_list
                and settings.ALL_SQUAD_PRICE is not None
                and Games.objects.filter(has_squad_entry=True).count()
                == squad_list.count("sq")):
            total_value = int(settings.ALL_SQUAD_PRICE)
            applied_internal_discount = True
        elif ("sq" not in squad_list and "so" in squad_list
              and settings.ALL_SOLO_PRICE is not None
              and Games.objects.filter(has_solo_entry=True).count()
              == squad_list.count("so")):
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
                        if squad_list.count(
                                squad_list[0]) == len(squad_list) and (
                                    squad_list[0] == "sq" and i.if_squad
                                    or squad_list[0] == "so" and i.if_solo):
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
        # Towards Payments
        if total_value > 0:
            request.session["order_list"] = order_list
            request.session["total_value"] = total_value
            currency = "INR"
            purpose = str(uuid.uuid4())
            request.session["purpose"] = purpose
            current_site = get_current_site(request)
            razorpay_order = razorpay_client.order.create(
                dict(
                    amount=total_value * 100,
                    currency=currency,
                    receipt=purpose,
                    notes={"order_list": str(order_list)},
                    payment_capture="0",
                ))
            pay = Payments(
                order_id=purpose,
                order_id_merchant=razorpay_order["id"],
                amount=int(total_value),
                orders_list=str(order_list),
            )
            pay.save()
            request.user.orders.add(pay)
            return render(
                request,
                "checkout.html",
                {
                    "total_value":
                    total_value,
                    "action_url":
                    "?",
                    "title":
                    "Pay for the Games that you want to participate",
                    "undiscounted_value":
                    undiscounted_value,
                    "applied_internal_discount":
                    applied_internal_discount,
                    "purpose":
                    purpose,
                    # Razorpay
                    "razorpay_order_id":
                    razorpay_order["id"],
                    "razorpay_merchant_key":
                    settings.RAZOR_KEY_ID,
                    "razorpay_amount":
                    total_value * 100,
                    "currency":
                    currency,
                    "callback_url":
                    reverse("payment_stats"),
                    "image_url":
                    f"{request.scheme}://{current_site.domain}{settings.STATIC_URL}icons/logo.png",
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
@require_POST
@csrf_exempt
@login_required
@cache_page(60 * 15)
def payment_stats(request):
    payment_id = request.POST.get("razorpay_payment_id", "")
    razorpay_order_id = request.POST.get("razorpay_order_id", "")
    signature = request.POST.get("razorpay_signature", "")
    try:
        # verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature({
            "razorpay_order_id":
            razorpay_order_id,
            "razorpay_payment_id":
            payment_id,
            "razorpay_signature":
            signature,
        })
        if result is None:
            try:
                # capture the payemt
                razorpay_client.payment.capture(
                    payment_id,
                    int(request.session["total_value"]) * 100)
            except:
                messages.error(
                    request,
                    "Couldn't verify the payment signature!",
                )
                redirect_link = reverse("make_order")
                return render(
                    request,
                    "checkout.html",
                    {
                        "payafter": True,
                        "redirect_link": redirect_link,
                        "title": "Payment Status check or verifier",
                    },
                )
            order_list = request.session.get("order_list")
            pay = Payments.objects.filter(
                order_id=request.session["purpose"],
                order_id_merchant=razorpay_order_id,
                amount=int(request.session["total_value"]),
            ).get()
            pay.payment_id_merchant = payment_id
            pay.payment_status = "S"
            pay.save()
            messages.success(
                request,
                "You have successfully paid the amount! Please wait for 2secs")
            for i in order_list:
                game = Games.objects.filter(game_unique_id=i[0]).get()
                game_group = GameGroup(game=game,
                                       payment_id=pay,
                                       solo_or_squad=i[1])
                game_group.save()
                game_group.users.add(request.user)
            redirect_link = reverse("make_groups")
            current_site = get_current_site(request)
            ctx = {
                "user": request.user,
                "domain": current_site.domain,
                "username": request.user.username,
                "protocol": "https" if request.is_secure() else "http",
                "receipt_id": request.session.get("purpose"),
                "amount": request.session.get("total_value"),
            }
            if not EmailTemplate.objects.filter(name="payment_mail").exists():
                message = render_to_string("pay_mail.html")
                EmailTemplate.objects.create(
                    name="payment_mail",
                    description="Mail to send after payment",
                    subject="You have successfully made the payment for TGL - 2.0",
                    html_content=message,
                )
            mail.send(
                request.user.email,
                settings.EMAIL_HOST_USER,
                template="payment_mail",
                context=ctx,
            )
            mail_queue.delay()
    except Payments.DoesNotExist:
        messages.error(request, "The transaction does not exists")
        redirect_link = reverse("make_order")
    except:
        messages.error(
            request,
            "There was some error processing your payment! Please contact the support",
        )
        redirect_link = reverse("make_order")
    try:
        del request.session["order_list"]
    except:
        pass
    try:
        del request.session["purpose"]
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
@cache_page(60 * 15)
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


@sync_to_async
@login_required
@cache_page(60 * 15)
def get_detailed_invoice(request, order_id):
    try:
        payment_object = Payments.objects.filter(order_id=order_id).get()
        return render(
            request,
            "detailed_invoice.html",
            {
                "order_list": ast.literal_eval(payment_object.orders_list),
                "order_id": order_id,
                "payment_object": payment_object,
            },
        )
    except:
        raise PermissionDenied
