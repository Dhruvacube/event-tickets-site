"""
 It updates the pending payments which have been due for more than 10 mins
"""

from django.conf import settings
from django.core.management.base import BaseCommand
from django.timezone import now
import datetime

from payments.models import Payments


class Command(BaseCommand):
    help = "It updates the pending payments which have been due for more than 10 mins"
    requires_system_checks = output_transaction = requires_migrations_checks = True

    def handle(self, *args, **options):
        try:
            payments = Payments.objects.filter(payment_status="P").iterator()
            for i in payments:
                if i.created_at <= now() - datetime.timedelta(minutes=10):
                    i.payment_status = "F"
                    i.save()
            self.stdout.write(self.style.SUCCESS("Success"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
