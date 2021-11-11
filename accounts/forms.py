from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserChangeForm,
)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator
from django.template import loader
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from post_office import mail
from post_office.models import EmailTemplate

from main.tasks import mail_queue

from .models import User


def validate_email(email):
    occurences = User.objects.filter(email=str(email)).count()
    if occurences:
        raise ValidationError(
            _("%(email)s is already in use! Please use a different email."),
            params={"email": email},
        )


def validate_zip(value):
    if not value.isdigit():
        raise ValidationError(
            _("%(value)s is not a valid zip code"),
            params={"value": value},
        )
    list_value = value.split(" ")
    str_value = "".join(list_value)
    return str_value


def validate_city(value):
    if len(value) < 2:
        raise ValidationError(
            _("%(value)s is not a valid city name"),
            params={"value": value},
        )


def validate_address(value):
    if len(value) <= 1 or value.isnumeric():
        raise ValidationError(
            _("%(value)s is not a valid address"),
            params={"value": value},
        )


class SignupForm(forms.Form):
    first_name = forms.CharField(max_length=250)
    last_name = forms.CharField(max_length=250)
    email = forms.EmailField(max_length=200,
                             help_text="Required",
                             validators=[validate_email])
    gender = forms.ChoiceField(choices=(("M", "Male"), ("F", "Female"),
                                        ("O", "Others")), )
    phone = forms.CharField(
        max_length=15,
        validators=[MinLengthValidator(10)],
        help_text=_("It should be +91 67xxx"),
    )
    address = forms.CharField(validators=[validate_address],
                               widget=forms.Textarea)
    city = forms.CharField(max_length=500, validators=[validate_city])
    state = forms.CharField(max_length=250)
    country = forms.CharField(max_length=250)
    zip_code = forms.CharField(max_length=6, validators=[validate_zip])
    university_name = forms.CharField(max_length=250)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["required"] = "true"

        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["required"] = "true"

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["required"] = "true"

        # self.fields["registration_no"].widget.attrs["class"] = "form-control"

        self.fields["phone"].widget.attrs["class"] = "form-control"
        self.fields["phone"].widget.attrs["required"] = "true"

        self.fields["address"].widget.attrs["class"] = "form-control"
        self.fields["address"].widget.attrs["rows"] = "50"

        self.fields["city"].widget.attrs["class"] = "form-control"
        self.fields["city"].widget.attrs["required"] = "true"

        self.fields["state"].widget.attrs["class"] = "form-control"
        self.fields["state"].widget.attrs["required"] = "true"

        self.fields["country"].widget.attrs["class"] = "form-control"
        self.fields["country"].widget.attrs["required"] = "true"
        self.fields["country"].widget.attrs["value"] = "India"

        self.fields["zip_code"].widget.attrs["class"] = "form-control"

        self.fields["gender"].widget.attrs["class"] = "form-control"

        self.fields["university_name"].widget.attrs["class"] = "form-control"
        self.fields["university_name"].widget.attrs["required"] = "true"

        # self.fields["gender"].widget.attrs["style"] = "color: black !important; background-color: white !important;"


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ("username", "password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs[
            "placeholder"] = "Type in username"
        self.fields["username"].widget.attrs["class"] = "form-control"

        self.fields["password"].widget.attrs[
            "placeholder"] = "Type in your password"
        self.fields["password"].widget.attrs["class"] = "form-control"


class request_verification_mail(forms.Form):
    email = forms.EmailField(label="Your registered email address")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs[
            "placeholder"] = "Your registered email address"
        self.fields["email"].widget.attrs["class"] = "form-control"


UserModel = get_user_model()


class PasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs[
            "placeholder"] = "New Password"
        self.fields["new_password1"].widget.attrs[
            "class"] = "form-control mb-20"

        self.fields["new_password2"].widget.attrs[
            "placeholder"] = "Retype the new password"
        self.fields["new_password2"].widget.attrs[
            "class"] = "form-control mb-20"


class PasswordReset(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """Send mail"""
        if not EmailTemplate.objects.filter(name="password_reset").exists():
            message = render_to_string(html_email_template_name)

            subject = loader.render_to_string(subject_template_name, context)
            subject = "".join(subject.splitlines())

            EmailTemplate.objects.create(
                name="password_reset",
                description="This is the HTML email template for the password reset of the already existing account",
                subject=subject,
                html_content=message,
            )
        mail.send(
            to_email,
            from_email,
            template="password_reset",
            context=context,
        )
        mail_queue.delay()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Email address"
        self.fields["email"].widget.attrs["class"] = "form-control mb-20"
        self.fields["email"].label = "Your account email address"


class EditProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        if "admin" in kwargs:
            self.admin = kwargs["admin"]
            kwargs.pop("admin")
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["required"] = "true"

        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["required"] = "true"

        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["required"] = "true"

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["required"] = "true"

        # self.fields["registration_no"].widget.attrs["class"] = "form-control"

        self.fields["phone"].widget.attrs["class"] = "form-control"
        self.fields["phone"].widget.attrs["required"] = "true"

        self.fields["address1"].widget.attrs["class"] = "form-control"
        self.fields["address1"].widget.attrs["required"] = "true"

        self.fields["address2"].widget.attrs["class"] = "form-control"

        self.fields["city"].widget.attrs["class"] = "form-control"
        self.fields["city"].widget.attrs["required"] = "true"

        self.fields["state"].widget.attrs["class"] = "form-control"
        self.fields["state"].widget.attrs["required"] = "true"

        self.fields["country"].widget.attrs["class"] = "form-control"
        self.fields["country"].widget.attrs["required"] = "true"

        self.fields["zip_code"].widget.attrs["class"] = "form-control"
        self.fields["zip_code"].widget.attrs["required"] = "true"

        self.fields["gender"].widget.attrs["class"] = "form-control"
        self.fields["gender"].widget.attrs[
            "style"] = "color: black !important;"

        self.fields["university_name"].widget.attrs["class"] = "form-control"
        self.fields["university_name"].widget.attrs["required"] = "true"

        if not self.admin:
            self.fields.pop("password")

    class Meta(UserChangeForm):
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            # "registration_no",
            "email",
            "gender",
            "phone",
            "address1",
            "address2",
            "city",
            "state",
            "country",
            "zip_code",
            "university_name",
        )


class PasswordChangeForms(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].widget.attrs[
            "placeholder"] = "Current Password"
        self.fields["old_password"].widget.attrs[
            "class"] = "form-control mb-20"
        self.fields["old_password"].label = "Current Password"

        self.fields["new_password1"].widget.attrs[
            "placeholder"] = "New Password"
        self.fields["new_password1"].widget.attrs[
            "class"] = "form-control mb-10 "

        self.fields["new_password2"].widget.attrs[
            "placeholder"] = "Retype the new password"
        self.fields["new_password2"].widget.attrs[
            "class"] = "form-control mb-10 "
