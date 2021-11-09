from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import (
    ChoiceDropdownFilter,
    RelatedDropdownFilter,
)

from .models import *

# Register your models here.


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = (
        "order_id",
        "payment_id_merchant",
        "order_id_merchant",
        "amount",
        "payment_status",
    )
    list_filter = (("payment_status", ChoiceDropdownFilter),)
    search_fields = list_display + ("orders_list",)
    readonly_fields = (
        "orders_list",
        "created_at",
        "payment_id_merchant",
        "order_id_merchant",
        "order_id",
    )
    list_per_page = 30

    fieldsets = (
        (
            _("Order ID"),
            {"fields": ("order_id", "payment_id_merchant",
                        "order_id_merchant")},
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


@admin.register(ComboOffers)
class ComboOfferAdmin(admin.ModelAdmin):
    list_display = ("combo_id", "if_squad", "squad", "if_solo", "solo")
    list_filter = ("if_squad", "if_solo", ("games", RelatedDropdownFilter))
    list_per_page = 30

    readonly_fields = ("combo_id",)

    fieldsets = (
        (
            _("Combo Offer"),
            {
                "fields": (
                    "combo_id",
                    "games",
                )
            },
        ),
        (
            _("Solo"),
            {
                "fields": (
                    "if_solo",
                    "solo",
                )
            },
        ),
        (
            _("Squad"),
            {
                "fields": (
                    "if_squad",
                    "squad",
                )
            },
        ),
    )
