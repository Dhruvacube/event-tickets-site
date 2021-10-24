import os

from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import Group
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter

from .models import *


def retrivejsfile():
    # if settings.DEBUG:
    #     return ("js/richTextEditor.js", )
    # return (
    #     "https://tanzanite-lpu.github.io/tgl-2.0.0/main/static/js/richtexteditor.js",
    # )
    return ("js/richtexteditor.js",)


# Register your models here.
class GamesAdmin(admin.ModelAdmin):
    list_display = ("name", "platform", "solo_entry",
                    "squad_entry", "image_url")
    list_filter = (("platform", ChoiceDropdownFilter),)
    search_fields = list_display + list_filter
    readonly_fields = ("view_image",)
    list_per_page = 15

    fieldsets = (
        (_("Name"), {"fields": ("name",)}),
        (_("Description"), {
         "fields": ("short_description", "long_description")}),
        (_("Image"), {"fields": ("image_url",) + readonly_fields}),
        (_("Platform"), {"fields": ("platform",)}),
        (_("Solo Entry"), {"fields": ("has_solo_entry", "solo_entry")}),
        (
            _("Squad Entry"),
            {"fields": ("has_squad_entry", "squad_entry",
                        "squad_entry_members")},
        ),
    )

    class Media:
        js = retrivejsfile()


class GameGroupAdmin(admin.ModelAdmin):
    list_display = (
        "group_unique_id",
        "group_name",
        "solo_or_squad",
        "game",
        "payment_id",
    )
    list_filter = (("solo_or_squad", ChoiceDropdownFilter), "game")
    search_fields = list_display + list_filter
    list_per_page = 30

    fieldsets = (
        (_("Name"), {"fields": ("group_name", "group_unique_id")}),
        (_("Mode"), {"fields": ("solo_or_squad",)}),
        (_("Game"), {"fields": ("game",)}),
        (_("Users"), {"fields": ("users",)}),
        (_("Payment ID"), {"fields": ("payment_id",)}),
    )


class SponserAdmin(admin.ModelAdmin):
    list_display = search_fields = ("name", "website", "image")
    readonly_fields = ("view_image",)
    list_per_page = 10

    fieldsets = (
        (_("Name"), {"fields": ("name",)}),
        (_("Details"), {"fields": ("website", "image", "view_image")}),
    )


admin.site.register(Sponser, SponserAdmin)
admin.site.register(Games, GamesAdmin)
admin.site.register(GameGroup, GameGroupAdmin)
admin.site.unregister(Group)
admin.site.site_header = admin.site.site_title = "Tanzanite Gaming League 2.0"
