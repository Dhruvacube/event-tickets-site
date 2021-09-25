from post_office.models import EmailTemplate
from post_office import mail
from django.template.loader import render_to_string
from django.template import loader
from django.contrib.auth.forms import (PasswordChangeForm, PasswordResetForm,
                                       SetPasswordForm, UserChangeForm)
from django.contrib.auth import get_user_model
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import User


def validate_email(email):
    occurences = User.objects.filter(email=str(email)).count()
    if occurences:
        raise ValidationError(
            _('%(email)s is already in use! Please use a different email.'),
            params={'email': email},
        )


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200, help_text='Required', validators=[validate_email])

    class Meta(UserCreationForm):
        model = User
        fields = (
            'username',
            'first_name', 
            'last_name',
            'registration_no', 
            'email', 
            'password1', 
            'password2', 
            'gender', 
            'phone', 
            'address1', 
            'address2', 
            'city', 
            'state', 
            'country',
            'zip_code'
        )

    def save(self, commit=True):
        user = super(SignupForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["required"] = "true"
        
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["required"] = "true"
        
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["required"] = "true"

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["required"] = "true"
        
        self.fields["registration_no"].widget.attrs["class"] = "form-control"
        self.fields["registration_no"].widget.attrs["required"] = "true"

        self.fields["password1"].widget.attrs["class"] = "form-control"
        self.fields["password1"].widget.attrs["required"] = "true"
        
        self.fields["password2"].widget.attrs["class"] = "form-control"
        self.fields["password2"].widget.attrs["required"] = "true"
        
        self.fields["phone"].widget.attrs["class"] = "form-control"
        self.fields["phone"].widget.attrs["required"] = "true"
        
        self.fields["address1"].widget.attrs["class"] = "form-control"
        self.fields["address1"].widget.attrs["required"] = "true"
        self.fields["address1"].widget.attrs["rows"] = "50"
        
        self.fields["address2"].widget.attrs["class"] = "form-control"
        self.fields["address2"].widget.attrs["required"] = "false"
        self.fields["address2"].widget.attrs["rows"] = "50"
        
        self.fields["city"].widget.attrs["class"] = "form-control"
        self.fields["city"].widget.attrs["required"] = "true"
        
        self.fields["state"].widget.attrs["class"] = "form-control"
        self.fields["state"].widget.attrs["required"] = "true"
        
        self.fields["country"].widget.attrs["class"] = "form-control"
        self.fields["country"].widget.attrs["required"] = "true"
        
        self.fields["zip_code"].widget.attrs["class"] = "form-control"
        self.fields["zip_code"].widget.attrs["required"] = "true"
        
        self.fields["gender"].widget.attrs["class"] = "form-control"
        self.fields["gender"].widget.attrs["style"] = "color: black !important; background-color: white !important;"

class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Type in username"
        self.fields["username"].widget.attrs["class"] = "form-control"

        self.fields["password"].widget.attrs["placeholder"] = "Type in your password"
        self.fields["password"].widget.attrs["class"] = "form-control"


class request_verification_mail(forms.Form):
    email = forms.EmailField(label="Your registered email address")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Your registered email address"
        self.fields["email"].widget.attrs["class"] = "form-control"


UserModel = get_user_model()


class PasswordResetConfirmForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["new_password1"].widget.attrs["placeholder"] = "New Password"
        self.fields["new_password1"].widget.attrs["class"] = "form-control mb-20"

        self.fields["new_password2"].widget.attrs["placeholder"] = "Retype the new password"
        self.fields["new_password2"].widget.attrs["class"] = "form-control mb-20"


class PasswordReset(PasswordResetForm):
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        '''Send mail'''

        if not EmailTemplate.objects.filter(name='password_reset').all():
            message = render_to_string(html_email_template_name)

            subject = loader.render_to_string(subject_template_name, context)
            subject = ''.join(subject.splitlines())

            EmailTemplate.objects.create(
                name='password_reset',
                description="This is the HTML email template for the password reset of the already existing account",
                subject=subject,
                html_content=message,
            )

        mail.send(
            to_email,
            from_email,
            template='password_reset',
            context=context,
            priority='now'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].widget.attrs["placeholder"] = "Email address"
        self.fields["email"].widget.attrs["class"] = "form-control mb-20"
        self.fields['email'].label = "Your account email address"


class EditProfileForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control"
        self.fields["username"].widget.attrs["required"] = "true"
        
        self.fields["first_name"].widget.attrs["class"] = "form-control"
        self.fields["first_name"].widget.attrs["required"] = "true"
        
        self.fields["last_name"].widget.attrs["class"] = "form-control"
        self.fields["last_name"].widget.attrs["required"] = "true"

        self.fields["email"].widget.attrs["class"] = "form-control"
        self.fields["email"].widget.attrs["required"] = "true"
        
        self.fields["registration_no"].widget.attrs["class"] = "form-control"
        self.fields["registration_no"].widget.attrs["required"] = "true"
        
        self.fields["phone"].widget.attrs["class"] = "form-control"
        self.fields["phone"].widget.attrs["required"] = "true"
        
        self.fields["address1"].widget.attrs["class"] = "form-control"
        self.fields["address1"].widget.attrs["required"] = "true"
        self.fields["address1"].widget.attrs["rows"] = "50"
        
        self.fields["address2"].widget.attrs["class"] = "form-control"
        self.fields["address2"].widget.attrs["required"] = "true"
        self.fields["address2"].widget.attrs["rows"] = "50"
        
        self.fields["city"].widget.attrs["class"] = "form-control"
        self.fields["city"].widget.attrs["required"] = "true"
        
        self.fields["state"].widget.attrs["class"] = "form-control"
        self.fields["state"].widget.attrs["required"] = "true"
        
        self.fields["country"].widget.attrs["class"] = "form-control"
        self.fields["country"].widget.attrs["required"] = "true"
        
        self.fields["zip_code"].widget.attrs["class"] = "form-control"
        self.fields["zip_code"].widget.attrs["required"] = "true"
        
        self.fields["gender"].widget.attrs["class"] = "form-control"
        self.fields["gender"].widget.attrs["style"] = "color: black !important;"
        
        self.fields["unique_id"].widget.attrs["class"] = "form-control"
        self.fields["unique_id"].widget.attrs["disabled"] = "true"
        
        self.fields["password"].widget.attrs["class"] = "d-none d-print-none"
        self.fields["password"].widget.attrs["style"] = "display: none;"

    class Meta(UserChangeForm):
        model = User
        model = User
        fields = (
            'username',
            'first_name', 
            'last_name',
            'registration_no', 
            'email', 
            'gender', 
            'phone', 
            'address1', 
            'address2', 
            'city', 
            'state', 
            'country',
            'zip_code',
            'unique_id'
        )


class PasswordChangeForms(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["old_password"].widget.attrs["placeholder"] = "Current Password"
        self.fields["old_password"].widget.attrs["class"] = "form-control mb-20"
        self.fields['old_password'].label = "Current Password"

        self.fields["new_password1"].widget.attrs["placeholder"] = "New Password"
        self.fields["new_password1"].widget.attrs["class"] = "form-control mb-10 "

        self.fields["new_password2"].widget.attrs["placeholder"] = "Retype the new password"
        self.fields["new_password2"].widget.attrs["class"] = "form-control mb-10 "
