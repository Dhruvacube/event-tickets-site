from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from .views import *

urlpatterns = [
     path("make_order/", make_order, name="make_order"),
     re_path(r"^payment_stats", payment_stats, name="payment_stats"),
     path("view_payments_history/",view_payments_history,name="view_payments_history"),
     path("update_all_payments_admin/",update_payments,name="update_all_payments_admin"),
     path("get_detailed_invoice/<uuid:order_id>",get_detailed_invoice, name="get_detailed_invoice"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
