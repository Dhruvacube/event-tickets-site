from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import *

# Register your models here.


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = search_fields = (
        "referral_code",
        "name",
        "description",
        "discount_percentage",
    )
    readonly_fields = ("referral_code", )
    list_per_page = 20

    fieldsets = (
        (
            _("Code"),
            {
                "fields": ("referral_code", )
            },
        ),
        (_("Details"), {
            "fields": ("name", "description", "discount_percentage")
        }),
    )
