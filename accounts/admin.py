from django import forms
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from .forms import SignupForm
from .models import User


class CustomUserAdmin(UserAdmin):
    add_form = SignupForm
    model = User
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
            )
        },
    ), ) + (UserAdmin.fieldsets[2], UserAdmin.fieldsets[3]) + ((_("Orders"), {
        "fields": ("orders", )
    }), ))
    search_fields = UserAdmin.search_fields + (
        "registration_no",
        "phone",
        "address1",
        "address2",
        "state",
        "city",
        "zip_code",
        "gender",
        "amount",
        "orders",
        "referral_code",
    )
    verbose_name_plural = "Profile"
    readonly_fields = ("unique_id", )


admin.site.register(User, CustomUserAdmin)
