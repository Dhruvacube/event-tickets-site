from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Payments(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text=_('The order ID by which the system refers'))
    order_id_instamojo = models.UUIDField(default=uuid.uuid4,help_text=_('The order ID by which the INSTAMOJO refers'))
    amount = models.IntegerField()
    payment_status = models.CharField(max_length=250,help_text=_('The status of payment'),choices=(('P','Pending'),('F','Failed'),('S','Success')), default='P')
    orders_list = models.TextField(help_text=_('The orders list value'))
    
    def __str__(self):
        return str(self.order_id)
    
    
