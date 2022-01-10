import secrets
import string
import uuid

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _


def generate_combo_code():
    return "".join(
        secrets.choice(string.ascii_letters + string.digits +
                       str(secrets.randbits(7))) for i in range(5)).upper()


class Payments(models.Model):
    order_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text=_("The order ID by which the system refers"),
    )
    payment_id_merchant = models.CharField(
        default=uuid.uuid4,
        help_text=_("The Payment ID by which the Razorpay refers"),
        null=True,
        blank=True,
        max_length=250,
    )
    order_id_merchant = models.CharField(
        help_text=_("The Order ID by which the Razorpay refers"),
        null=True,
        blank=True,
        max_length=250,
    )
    amount = models.IntegerField()
    payment_status = models.CharField(
        max_length=250,
        help_text=_("The status of payment"),
        choices=(("P", "Pending"), ("F", "Failed"), ("S", "Success"), ("R", "Refund Done")),
        default="P",
    )
    orders_list = models.TextField(help_text=_("The orders list value"))
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.order_id)

    class Meta:
        verbose_name_plural = "Payments"
        ordering = ("-created_at", )


class ComboOffers(models.Model):
    combo_id = models.CharField(
        default=generate_combo_code,
        help_text=_("The Combo ID by which the system refers"),
        max_length=250,
        unique=True,
    )
    games = models.ManyToManyField("main.Games")
    if_squad = models.BooleanField(default=True,
                                   help_text=_("If Squad Option is there"))
    squad = models.IntegerField(default=0)
    if_solo = models.BooleanField(default=True,
                                  help_text=_("If Solo Option is there"))
    solo = models.IntegerField(default=0)

    def __str__(self):
        return f"Combo Offer - {self.combo_id}"

    class Meta:
        verbose_name_plural = "Combo Offers"
