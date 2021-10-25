from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter

from .models import *

# Register your models here.


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "request_id_instamojo",
        "instamojo_order_id",
        "amount",
        "payment_status",
    )
    list_filter = (("payment_status", ChoiceDropdownFilter),)
    search_fields = list_display + list_filter + ("orders_list",)
    readonly_fields = (
        "orders_list",
        "created_at",
        "request_id_instamojo",
        "instamojo_order_id",
        "order_id",
    )
    list_per_page = 30

    fieldsets = (
        (
            _("Order ID"),
            {"fields": ("order_id", "request_id_instamojo",
                        "instamojo_order_id")},
        ),
        (_("Amount"), {"fields": ("amount",)}),
        (
            _("Status"),
            {
                "fields": (
                    "payment_status",
                    "created_at",
                )
            },
        ),
        (_("Orders List"), {"fields": ("orders_list",)}),
    )
