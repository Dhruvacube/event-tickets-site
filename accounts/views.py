import functools
import os
from datetime import datetime

import requests
from asgiref.sync import sync_to_async
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (
    PasswordResetConfirmView,
    PasswordResetDoneView,
    PasswordResetView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from post_office import mail
from post_office.models import EmailTemplate

from referral.models import Referral

from .decorators import check_recaptcha
from .forms import (
    EditProfileForm,
    LoginForm,
    PasswordChangeForms,
    PasswordReset,
    PasswordResetConfirmForm,
    SignupForm,
    request_verification_mail,
)
from .models import User
from .templatetags import getfunc
from .tokens import account_activation_token


# Create your views here.
class PasswordResetConfirmViews(PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm


class PasswordResetViews(PasswordResetView):
    html_email_template_name = "registration/password_reset_email.html"
    form_class = PasswordReset
    title = _("Password reset")
    description = _(
        "Password Reset for the existing account for the Tanzanite Gaming League 2.0"
    )

    @functools.lru_cache(maxsize=4)
    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": settings.EMAIL_HOST_USER,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


class PasswordResetDoneViews(PasswordResetDoneView):
    template_name = "registration/password_reset_done.html"
    title = _("Password reset sent")


@sync_to_async
@login_required
def view_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)
            referral = request.POST.get("referral_code")
            if len(referral) == 0 or referral in [None, ""]:
                user.referral_code = None
            else:
                if Referral.objects.filter(referral_code=referral).exists():
                    request.user.referral_code = Referral.objects.filter(
                        referral_code=referral
                    ).get()
                else:
                    messages.warning(
                        request,
                        f"<strong>{referral}</strong> Referral Code does not exists",
                    )

            messages.success(
                request, "Your <strong>Profile</strong> has been update successfully !"
            )
            form.save(commit=True)
            return redirect(reverse("view_profile"))
        if not form.errors:
            messages.error(
                request, "Please correct the errors mentioned below!")

    else:
        form = EditProfileForm(instance=request.user)
    return render(
        request,
        "accounts/signup_and_different_template.html",
        {
            "form": form,
            "heading": "Update Profile",
            "title": "Update Profile",
            "view_profile": True,
            "no_display_messages": True,
            "referral": True,
        },
    )


@sync_to_async
@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForms(data=request.POST, user=request.user)

        if form.is_valid():
            messages.success(
                request, "Your <strong>password</strong> has been update successfully !"
            )
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponsePermanentRedirect(reverse("change_password"))
        messages.error(request, "Please correct the errors mentioned below!")
    else:
        form = PasswordChangeForms(user=request.user)
    return render(
        request,
        "accounts/signup_and_different_template.html",
        {
            "form": form,
            "heading": "Change Password",
            "no_display_messages": True,
            "title": "Change Password",
        },
    )


@sync_to_async
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
    return HttpResponsePermanentRedirect(reverse("home"))


@sync_to_async
def loginform(request):
    if request.method == "POST":
        form = LoginForm(request=request, data=request.POST)

        username = request.POST.get("username")
        if not User.objects.filter(username=username).exists():
            messages.warning(request, "Please create an new account !")
            return redirect(reverse("signin"))
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return HttpResponsePermanentRedirect(reverse("home"))
            messages.error(request, "Invalid username or password.")
            return redirect(reverse("signin"))
        messages.error(request, "Details Invalid")
        return redirect(reverse("signin"))
    form = LoginForm()
    return render(
        request,
        "login.html",
        {
            "title": "Login",
            "form": form,
        },
    )


@sync_to_async
def signup(request):
    current_site = get_current_site(request)
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True

            referral = request.POST.get("referral_code")
            if len(referral) == 0 or referral in [None, ""]:
                user.referral_code = None
            elif Referral.objects.filter(referral_code=referral).exists():
                user.referral_code = Referral.filter(
                    referral_code=referral).get()
            else:
                messages.warning(
                    request,
                    f"<strong>{referral}</strong> Referral Code does not exists",
                )
            user.save()
            to_email = form.cleaned_data.get("email")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")

            ctx = {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
                "username": username,
                "password": password1,
                "protocol": "https" if request.is_secure() else "http",
            }
            if not EmailTemplate.objects.filter(name="register_mail").all():
                message = render_to_string("accounts/register_mail.html")
                mail_subject = "Thanks for Registering for TGL-2.0"
                EmailTemplate.objects.create(
                    name="register_mail",
                    description="Thank you E-Mail Template",
                    subject=mail_subject,
                    html_content=message,
                )
            mail.send(
                to_email,
                settings.EMAIL_HOST_USER,
                template="register_mail",
                context=ctx,
            )
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            messages.success(request, "Account created")
            return redirect(reverse("make_order"))
        message_error_list = []
        if form.errors.as_data():
            for i in form.errors.as_data():
                message = "\n".join(form.errors.as_data()[i][0].messages)
                message_error_list.append(message)
            for i in message_error_list:
                messages.error(request, i)
    form = SignupForm()
    return render(
        request,
        "accounts/signup_and_different_template.html",
        {
            "title": "Register Now",
            "form": form,
            "heading": "Register Now",
            "link_name": "Log In",
            "link": f'{reverse("signin")}',
            "domain": current_site.domain,
            "display": True,
            "referral": True,
            "no_display_messages": True,
        },
    )
