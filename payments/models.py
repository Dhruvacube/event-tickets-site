from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Payments(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    amount = models.IntegerField()
    payment_status = models.CharField(max_length=250,help_text=_('The status of payment'))
    orders_json = models.TextField(help_text=_('The orders json value'))
    
    def __str__(self):
        return str(self.order_id)
    
    
