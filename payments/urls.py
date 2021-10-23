from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path("make_order/", make_order, name="make_order"),
    path("create_payment/", create_payment, name="create_payment"),
    url(r"^payment_stats", payment_stats, name="payment_stats"),
    path("view_payments_history/", view_payments_history,
         name="view_payments_history"),
    path("update_all_payments_admin/", update_payments, name="update_all_payments_admin")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
