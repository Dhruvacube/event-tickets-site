from django.contrib.auth.models import AbstractUser, User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from localflavor.in_.models import INStateField
from django.core.validators import MinLengthValidator, MaxLengthValidator
from main.models import Games
from payments.models import Payments


# Create your models here.
def validate_zip(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s is not a valid zip code'),
            params={'value': value},
        )
    else:
        list_value=value.split(' ')
        str_value=''
        for i in list_value:
            str_value+=i
        return str_value    

def validate_city(value):
    if len(value) < 2:
        raise ValidationError(
            _('%(value)s is not a valid city name'),
            params={'value': value},
        )

def validate_address(value):
    if len(value) <= 1 or value.isnumeric():
        raise ValidationError(
            _('%(value)s is not a valid address'),
            params={'value': value},
        )

def validate_phone(value):
    for i in str(value[1:]):
        if i.isspace(): pass
        
        elif not i.strip(' ').isdigit():
            raise ValidationError(
                _(f'{value} is not a valid phone number'),
                params={'value': i},
            )
    if not value.strip(' ')[0] in '+':
        raise ValidationError(
            _(f'{value} is not a phone number, Please enter a no like +91 67xxxxxxxx'),
            params={'value': value},
        )


class User(AbstractUser):
    gender = models.CharField(max_length=11,choices=(('M','Male'),('F','Female'),('O','Others')), null=True)
    phone = models.CharField(_('phone'),max_length=15, validators=[MinLengthValidator(13),validate_phone])
    address1 = models.TextField(_('address 1'), validators=[validate_address])
    address2 = models.TextField(_('address 2') ,validators=[validate_address])
    city = models.CharField(_('city'),max_length=500, validators=[validate_city])
    state = INStateField(_('state'))
    zip_code = models.CharField(_('zip code'),max_length=6,validators=[validate_zip])
    registration_no = models.IntegerField(_('Registration No'),validators=[MinLengthValidator(5),MaxLengthValidator(10)], null=True)
    amount = models.DecimalField(help_text=_('Amount paid by the person/team'),max_digits=19, decimal_places=10, null=True)
    orders = models.ForeignKey(Payments ,on_delete=models.CASCADE, help_text=_('This is to be filled by computer'), null=True)

    class Meta:
        unique_together = ('email','registration_no')


class GameGroup(models.Model):
    games=models.ManyToManyField(Games)
    users=models.ManyToManyField(User)
    payment_id = models.ForeignKey(Payments ,on_delete=models.CASCADE, help_text=_('This is to be filled by computer'))
    