from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

from .models import *


def retrivejsfile():
    return ("js/richTextEditorAnnouncements.js", )


@admin.register(GlobalAnnouncements)
class GlobalAnnouncementsAdmin(admin.ModelAdmin):
    list_display = (
        "announcement_id",
        "announcement_heading",
        "announncement_creation_date",
        "publish",
    )
    list_filter = ("announncement_creation_date", "publish")
    search_fields = list_display[:-1] + list_filter
    readonly_fields = ("announncement_creation_date", "announcement_id")
    list_per_page = 20

    fieldsets = (
        (_("Id"), {
            "fields": ("announcement_id", )
        }),
        (
            _("Message"),
            {
                "fields": (
                    "announcement_heading",
                    "announncement_message",
                )
            },
        ),
        (_("Creation"), {
            "fields": list_filter
        }),
    )

    def publish_announcement(self, request, queryset):
        updated = queryset.update(publish=True)
        self.message_user(
            request,
            ngettext(
                "%d announcement was succesfully published",
                "%d announcements were succesfully published",
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    publish_announcement.short_description = "Publish Announcements"

    def unpublish_announcement(self, request, queryset):
        updated = queryset.update(publish=False)
        self.message_user(
            request,
            ngettext(
                "%d announcement was succesfully unpublished",
                "%d announcements were succesfully unpublished",
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    unpublish_announcement.short_description = "Unpublish Announcements"

    # Registering the custom actions
    actions = [publish_announcement, unpublish_announcement]

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    class Media:
        js = retrivejsfile()


@admin.register(GroupsAnnouncements)
class GroupsAnnouncementsAdmin(admin.ModelAdmin):
    list_display = (
        "announcement_id",
        "announcement_heading",
        "announncement_creation_date",
        "publish",
    )
    list_filter = ("announncement_creation_date", "publish")
    search_fields = list_display[:-1] + list_filter
    readonly_fields = ("announncement_creation_date", "announcement_id")
    list_per_page = 20

    fieldsets = (
        (_("Id"), {
            "fields": ("announcement_id", )
        }),
        (
            _("Message"),
            {
                "fields": (
                    "announcement_heading",
                    "announncement_message",
                )
            },
        ),
        (_("Groups"), {
            "fields": ("groups", )
        }),
        (_("Creation"), {
            "fields": list_filter
        }),
    )

    def publish_announcement(self, request, queryset):
        updated = queryset.update(publish=True)
        self.message_user(
            request,
            ngettext(
                "%d announcement was succesfully published",
                "%d announcements were succesfully published",
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    publish_announcement.short_description = "Publish Announcements"

    def unpublish_announcement(self, request, queryset):
        updated = queryset.update(publish=False)
        self.message_user(
            request,
            ngettext(
                "%d announcement was succesfully unpublished",
                "%d announcements were succesfully unpublished",
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    unpublish_announcement.short_description = "Unpublish Announcements"

    # Registering the custom actions
    actions = [publish_announcement, unpublish_announcement]

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    class Media:
        js = retrivejsfile()


@admin.register(UsersAnnouncements)
class UsersAnnouncementsAdmin(admin.ModelAdmin):
    list_display = (
        "announcement_id",
        "announcement_heading",
        "announncement_creation_date",
        "publish",
    )
    list_filter = ("announncement_creation_date", "publish")
    search_fields = list_display[:-1] + list_filter
    readonly_fields = ("announncement_creation_date", "announcement_id")
    list_per_page = 20

    fieldsets = (
        (_("Id"), {
            "fields": ("announcement_id", )
        }),
        (
            _("Message"),
            {
                "fields": (
                    "announcement_heading",
                    "announncement_message",
                )
            },
        ),
        (_("Users"), {
            "fields": ("users", )
        }),
        (_("Creation"), {
            "fields": list_filter
        }),
    )

    def publish_announcement(self, request, queryset):
        updated = queryset.update(publish=True)
        self.message_user(
            request,
            ngettext(
                "%d announcement was succesfully published",
                "%d announcements were succesfully published",
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    publish_announcement.short_description = "Publish Announcements"

    def unpublish_announcement(self, request, queryset):
        updated = queryset.update(publish=False)
        self.message_user(
            request,
            ngettext(
                "%d announcement was succesfully unpublished",
                "%d announcements were succesfully unpublished",
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    unpublish_announcement.short_description = "Unpublish Announcements"

    # Registering the custom actions
    actions = [publish_announcement, unpublish_announcement]

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff

    class Media:
        js = retrivejsfile()
