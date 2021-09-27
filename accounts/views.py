from .tokens import account_activation_token
from asgiref.sync import sync_to_async
from .forms import LoginForm, SignupForm, request_verification_mail
from post_office.models import EmailTemplate
from post_office import mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from datetime import datetime
import os

import requests
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import (PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .decorators import check_recaptcha
from .forms import (EditProfileForm, PasswordChangeForms, PasswordReset,
                    PasswordResetConfirmForm)
from .models import User


# Create your views here.
class PasswordResetConfirmViews(PasswordResetConfirmView):
    form_class = PasswordResetConfirmForm


class PasswordResetViews(PasswordResetView):
    html_email_template_name = 'registration/password_reset_email.html'
    form_class = PasswordReset
    title = _('Password reset')
    description = _(
        'Password Reset for the existing account for the 24 Ave Pizza')

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': 'dhruvashaw@gmail.com',
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
            'extra_email_context': self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)


class PasswordResetDoneViews(PasswordResetDoneView):
    template_name = 'registration/password_reset_done.html'
    title = _('Password reset sent')


@sync_to_async
@login_required
def view_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            messages.success(
                request, "Your <strong>Profile</strong> has been update successfully !")
            form.save()
            return redirect(reverse('view_profile'))
        else: messages.error(request, "Please correct the errors mentioned below!")

    else:
        form = EditProfileForm(instance=request.user)
    return render(
        request, 
        'accounts/signup_and_different_template.html', 
        {
            'form': form,
            'heading': 'Update Profile'
        }
    )


@sync_to_async
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForms(data=request.POST, user=request.user)

        if form.is_valid():
            messages.success(
                request, "Your <strong>password</strong> has been update successfully !")
            form.save()
            update_session_auth_hash(request, form.user)
            return HttpResponsePermanentRedirect(reverse('change_password'))

        else: messages.error(request, "Please correct the errors mentioned below!")
    else:
        form = PasswordChangeForms(user=request.user)
    return render(
        request, 
        'accounts/signup_and_different_template.html', 
        {
            'form': form,
            'heading': 'Change Password',
            'display_messages': True
        }
    )


@sync_to_async
@login_required
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
    return HttpResponsePermanentRedirect(reverse('home'))


@sync_to_async
def loginform(request):
    if request.method == 'POST':
        form = LoginForm(request=request, data=request.POST)

        username = request.POST.get('username')
        try:
            user1 = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.warning(request, "Please create an new account !")
            return redirect(reverse('signin'))

        if not user1.is_active: 
            messages.warning(
                request, 
                "<strong>Please activate</strong> your account from the <strong>link</strong> sent to your <strong>email!</strong>"
                )
        elif form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(
                request, 
                username=username, 
                password=password
            )
            if user is not None:
                login(request, user)
                messages.info(
                request, 
                    f"You are now logged in as {username}"
                )
                return HttpResponsePermanentRedirect(reverse('home'))
            else: 
                messages.error(request, "Invalid username or password.")
        else: 
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()
    return render(
        request, 
        'login.html',
        {
        'title': '| Login |',
        'form': form,
    })

@sync_to_async
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.save()
            messages.success(request, 'Account created')
            
        else:
            messages.error(request, 'There is some error please correct it!')
    else:
        form = SignupForm()
    current_site = get_current_site(request)
    return render(
        request, 
        'accounts/signup_and_different_template.html', 
        {
        'title': '| Register Now |',
        'form': form,
        'heading': 'Register Now',
        'link_name': 'Log In',
        'link': f'{reverse("signin")}',
        'domain': current_site.domain,
        "display": True
    })
