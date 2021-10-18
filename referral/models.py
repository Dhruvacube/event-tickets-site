from django.db import models
from django.utils.translation import gettext_lazy as _
import secrets
import string

def generate_referral_code():
    return ''.join(secrets.choice(string.ascii_letters + string.digits + str(secrets.randbits(7))) for i in range(5)).upper()


# Create your models here.
class Referral(models.Model):
    name = models.CharField(help_text=_('Name of the University / Person'), max_length=250)
    description = models.TextField(help_text=_('Optional'), blank=True, null=True)
    referral_code = models.CharField(max_length=250, unique=True, primary_key=True, default=generate_referral_code)
    discount_percentage = models.IntegerField(default=0)
    
    def __str__(self):
        return self.referral_code

