"""
 Command making referral code using the data from a csv file
 
 The csv should be there in 'main/static' and the filename should be 'data.csv'
 
 The csv data should be in the format of:
 email-id, name
 
 and the referral code will be mailled to them by the mail server and a csv file will be generated in 'main/static' under the name of 'new_data_generated.csv'
"""

import csv
import os

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from post_office import mail

from main.tasks import mail_queue
from referral.models import *


class Command(BaseCommand):
    help = "Command making referral code using the data from a csv file"
    requires_system_checks = output_transaction = requires_migrations_checks = True

    def handle(self, *args, **options):
        for i in Referral.objects.iterator():
            mail.send(
                i.description,
                settings.EMAIL_HOST_USER,
                subject="Your Unique Referral Link for Tanza Gaming League 2.0!",
                message=f'Hey {i.name.title()},\n Here is your unique "Referral Link" below:\nhttps://tanzanitelpu.com/accounts/signup/?referral={i.referral_code}',
            )
        mail_queue.delay()
