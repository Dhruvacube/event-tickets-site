from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_admin_listfilter_dropdown.filters import DropdownFilter

from .models import *


def retrivejsfile():
    # if settings.DEBUG:
    #     return ("js/richTextEditorAnnouncements.js",)
    # return (
    #     "https://tanzanite-lpu.github.io/tgl-2.0.0/announcements/static/js/richTextEditorAnnouncements.js",
    # )
    return ("js/richTextEditorAnnouncements.js",)


# Register your models here.


@admin.register(GlobalAnnouncements)
class GlobalAnnouncementsAdmin(admin.ModelAdmin):
    list_display = (
        "announcement_id",
        "announcement_heading",
        "announncement_creation_date",
    )
    list_filter = ("announncement_creation_date",)
    search_fields = list_display + list_filter
    readonly_fields = ("announncement_creation_date", "announcement_id")
    list_per_page = 20

    fieldsets = (
        (_("Id"), {"fields": ("announcement_id",)}),
        (
            _("Message"),
            {
                "fields": (
                    "announcement_heading",
                    "announncement_message",
                )
            },
        ),
        (_("Creation"), {"fields": list_filter}),
    )

    class Media:
        js = retrivejsfile()


@admin.register(GroupsAnnouncements)
class GroupsAnnouncementsAdmin(admin.ModelAdmin):
    list_display = (
        "announcement_id",
        "announcement_heading",
        "announncement_creation_date",
    )
    list_filter = ("announncement_creation_date",)
    search_fields = list_display + list_filter
    readonly_fields = ("announncement_creation_date", "announcement_id")
    list_per_page = 20

    fieldsets = (
        (_("Id"), {"fields": ("announcement_id",)}),
        (
            _("Message"),
            {
                "fields": (
                    "announcement_heading",
                    "announncement_message",
                )
            },
        ),
        (_("Groups"), {"fields": ("groups",)}),
        (_("Creation"), {"fields": list_filter}),
    )

    class Media:
        js = retrivejsfile()


@admin.register(UsersAnnouncements)
class UsersAnnouncementsAdmin(admin.ModelAdmin):
    list_display = (
        "announcement_id",
        "announcement_heading",
        "announncement_creation_date",
    )
    list_filter = ("announncement_creation_date",)
    search_fields = list_display + list_filter
    readonly_fields = ("announncement_creation_date", "announcement_id")
    list_per_page = 20

    fieldsets = (
        (_("Id"), {"fields": ("announcement_id",)}),
        (
            _("Message"),
            {
                "fields": (
                    "announcement_heading",
                    "announncement_message",
                )
            },
        ),
        (_("Users"), {"fields": ("users",)}),
        (_("Creation"), {"fields": list_filter}),
    )

    class Media:
        js = retrivejsfile()
