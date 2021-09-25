from django.shortcuts import render
from asgiref.sync import sync_to_async
import uuid
from django.views.decorators.http import require_GET, require_POST
from django.contrib.sites.shortcuts import get_current_site


# Create your views here.

def make_order(request):
    pass

@require_POST
@sync_to_async
def create_payment(request):
    amount = request.POST.get('amount')
    purpose = str(uuid.uuid4())
    buyers_name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    
    current_site = get_current_site(request)
    redirect_url = request.is_secure()
    
    allow_repeated_payments = False
    send_email = True
    send_sms = True
    expires_at = 600

@sync_to_async
def payment_stats(request):
    payment_id = request.GET.get('payment_id')
    payment_request_id = request.GET.get('payment_request_id')
    payment_status = request.GET.get('payment_status')