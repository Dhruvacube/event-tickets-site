from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import SignupForm
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    model = User
    list_display = UserAdmin.list_display + ("university_name", )
    fieldsets = ((UserAdmin.fieldsets[0], ) + ((
        _("Personal info"),
        {
            "fields":
            UserAdmin.fieldsets[1][1]["fields"] + (
                "unique_id",
                "university_name",
                "registration_no",
                "phone",
                "address1",
                "address2",
                "state",
                "city",
                "zip_code",
                "gender",
                "referral_code",
                "group_unique_id",
            )
        },
    ), ) + (UserAdmin.fieldsets[2], UserAdmin.fieldsets[3]) + ((_("Orders"), {
        "fields": ("orders", )
    }), ))
    search_fields = UserAdmin.search_fields + (
        "phone",
        "address1",
        "address2",
        "state",
        "city",
        "zip_code",
        "gender",
        "university_name",
        "unique_id",
    )
    verbose_name_plural = "Profile"
    readonly_fields = ("unique_id", "group_unique_id")

    def has_add_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_staff
