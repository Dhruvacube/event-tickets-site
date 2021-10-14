from django.db import models
import uuid
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from django.conf import settings

# Create your models here.


class Payments(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text=_(
        'The order ID by which the system refers'))
    request_id_instamojo = models.UUIDField(default=uuid.uuid4, help_text=_(
        'The Request ID by which the INSTAMOJO refers'))
    instamojo_order_id = models.CharField(help_text=_(
        'The order ID by which the INSTAMOJO refers'), null=True, blank=True, max_length=250)
    amount = models.IntegerField()
    payment_status = models.CharField(max_length=250, help_text=_('The status of payment'), choices=(
        ('P', 'Pending'), ('F', 'Failed'), ('S', 'Success')), default='P')
    orders_list = models.TextField(help_text=_('The orders list value'))
    created_at = models.DateTimeField(default=now)
    # payed_by = models.ForeignKey(settings.AUTH_USER_MODEL ,on_delete=models.CASCADE, help_text=_('This is to be filled by computer'))

    def __str__(self):
        return str(self.order_id)

    class Meta:
        verbose_name_plural = 'Payments'
        ordering = ('-created_at',)
