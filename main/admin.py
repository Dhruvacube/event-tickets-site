import os

from django.conf import settings
from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import Group
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django_admin_listfilter_dropdown.filters import ChoiceDropdownFilter

from .models import *


def retrivejsfile():
    return ("js/richtexteditor.js", )


@admin.register(Games)
class GamesAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "game_unique_id",
        "platform",
        "solo_entry",
        "squad_entry",
        "image_url",
    )
    list_filter = (("platform", ChoiceDropdownFilter), )
    search_fields = list_display + list_filter
    readonly_fields = ("view_image", "static_images_list", "game_unique_id")
    list_per_page = 15

    fieldsets = (
        (_("Name"), {
            "fields": ("game_unique_id", "name")
        }),
        (_("Description"), {
            "fields": ("short_description", "long_description")
        }),
        (_("Image"), {
            "fields": ("image_url", ) + (readonly_fields[0], )
        }),
        (_("Platform"), {
            "fields": ("platform", )
        }),
        (_("Solo Entry"), {
            "fields": ("has_solo_entry", "solo_entry")
        }),
        (
            _("Squad Entry"),
            {
                "fields":
                ("has_squad_entry", "squad_entry", "squad_entry_members")
            },
        ),
        (
            _("View the Sponsers Images in the backend"),
            {
                "classes": ("collapse", ),
                "fields": ("static_images_list", )
            },
        ),
    )

    class Media:
        js = retrivejsfile()


@admin.register(GameGroup)
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
    readonly_fields = ('group_unique_id',)
    list_per_page = 30

    fieldsets = (
        (_("Name"), {
            "fields": ("group_name", "group_unique_id")
        }),
        (_("Mode"), {
            "fields": ("solo_or_squad", )
        }),
        (_("Game"), {
            "fields": ("game", )
        }),
        (_("Users"), {
            "fields": ("users", )
        }),
        (_("Payment ID"), {
            "fields": ("payment_id", )
        }),
    )


@admin.register(Sponser)
class SponserAdmin(admin.ModelAdmin):
    list_display = search_fields = ("name", "website", "image")
    readonly_fields = ("view_image", "static_images_list")
    list_per_page = 10

    fieldsets = (
        (_("Name"), {
            "fields": ("name", )
        }),
        (_("Details"), {
            "fields": ("website", "image", "view_image")
        }),
        (
            _("View the Sponsers Images in the backend"),
            {
                "classes": ("collapse", ),
                "fields": ("static_images_list", )
            },
        ),
    )


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def delete_admin_logs(self, request, queryset):
        queryset.delete()

        self.message_user(
            request,
            ngettext(
                "%d log was successfully deleted.",
                "%d logs were successfully deleted.",
                len(queryset),
            ) % int(len(queryset)),
            messages.SUCCESS,
        )

    delete_admin_logs.short_description = (
        "Delete the selected ADMIN Logs without sticking")

    actions = [delete_admin_logs]


admin.site.unregister(Group)
admin.site.site_header = admin.site.site_title = "Tanzanite Gaming League 2.0"
