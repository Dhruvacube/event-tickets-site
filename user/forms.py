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
    email = forms.EmailField(max_length=200, help_text='Required',validators=[validate_email])
    
    class Meta(UserCreationForm):
        model = User
        fields = ('username', 'email','password1', 'password2')
    
    def save(self,commit=True):
        user = super(SignupForm,self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["placeholder"] = "Type in username"
        self.fields["username"].widget.attrs["class"] = "form-control"

        self.fields["email"].widget.attrs["placeholder"] = "Email Address"
        self.fields["email"].widget.attrs["class"] = "form-control"

        self.fields["password1"].widget.attrs["placeholder"] = "Create password"
        self.fields["password1"].widget.attrs["class"] = "form-control"

        self.fields["password2"].widget.attrs["placeholder"] = "Repeat password"
        self.fields["password2"].widget.attrs["class"] = "form-control"





class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username','password')
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