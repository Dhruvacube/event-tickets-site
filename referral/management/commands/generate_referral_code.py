"""
 Command making referral code using the data from a csv file
 
 The csv should be there in 'main/static' and the filename should be 'data.csv'
 
 The csv data should be in the format of:
 email-id, name
 
 and the referral ode will be mailled to them by the mail server and a csv file will be generated in 'main/static' under the name of 'new_data_generated.csv'
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
        file_path = settings.BASE_DIR / os.path.join("main", "static",
                                                     "data.csv")
        fields = ["E-Mail ID", "Name", "Referral Code"]
        data_to_write = []
        with open(file_path, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            for i in csvreader:
                if not Referral.objects.filter(description=i[0],
                                               name=i[1].title()).exists():
                    referral = Referral(description=i[0], name=i[1].title())
                    data_to_write.append({
                        "E-Mail ID":
                        i[0],
                        "Name":
                        i[1].title(),
                        "Referral Code":
                        referral.referral_code,
                    })
                    referral.save()
                    mail.send(
                        i[0],
                        settings.EMAIL_HOST_USER,
                        subject="Your Unique Referral Code for Tanza Gaming League 2.0!",
                        message=f'Hey {i[1].title()},\n Here is your unique "Referral Code" below:\n{referral.referral_code}',
                    )
        new_data_csv_file_path = settings.BASE_DIR / os.path.join(
            "main", "static", "new_data_generated.csv")
        with open(new_data_csv_file_path, "w") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data_to_write)
        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {len(data_to_write)} Referral(s) XD!"))
        self.stdout.write(
            self.style.SUCCESS(
                f"Exported the data to {settings.BASE_DIR / os.path.join('main', 'static', 'new_data_generated.csv')}"
            ))
        mail_queue.delay()
