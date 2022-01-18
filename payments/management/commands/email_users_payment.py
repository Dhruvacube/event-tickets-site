
from django.conf import settings
from django.core.management.base import BaseCommand
from post_office import mail

from accounts.models import User
from main.tasks import mail_queue

msg = """
Hey {first_name}, seems like you still haven't bought the tournament tickets for the Tanza Gaming League 2.0

Anyways you can buy the tickets from here https://tanzanitelpu.com/payments/make_order/
and the video explaining the whole process https://drive.google.com/file/d/1ocPPuVOReZkUMMwMf-77RjpqZZhErqGG/view?usp=sharing

If one of your team member has bought the ticket for you then you may ignore the message!

Anyways have a nice day!

Regards,
Team Tanzanite
"""


class Command(BaseCommand):
    help = (
        "It emails all those users data who haven't made any payment, failed or pending"
    )
    requires_system_checks = output_transaction = requires_migrations_checks = True

    def handle(self, *args, **options):
        try:
            users_iterator1 = User.objects.filter(
                orders__payment_status__in=["P", "F"],
                is_staff=False).values("first_name", "email")
            users_iterator2 = User.objects.filter(orders=None,
                                                  is_staff=False).values(
                                                      "first_name", "email")
            for i in users_iterator1.union(users_iterator2).iterator():
                mail.send(
                    i["email"],
                    settings.EMAIL_HOST_USER,
                    subject="Hey you still haven't bought the tickets for TGL-2.0!!!",
                    message=msg.format(first_name=i["first_name"]),
                )
            self.stdout.write(self.style.SUCCESS("Success"))
            mail_queue.delay()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
