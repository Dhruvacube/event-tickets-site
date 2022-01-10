import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from referral.models import *


class Command(BaseCommand):
    help = "Exports all the referral code data to a csv file"
    requires_system_checks = output_transaction = requires_migrations_checks = True

    def handle(self, *args, **options):
        new_data_csv_file_path = settings.BASE_DIR / os.path.join(
            "main", "static", "new_data_exported.csv")
        with open(new_data_csv_file_path, "w") as csvfile:
            writer = csv.DictWriter(csvfile,
                                    fieldnames=["Name", "Referral Code"])
            writer.writeheader()
            data_to_write = []
            for i in Referral.objects.iterator():
                data_to_write.append({
                    "Name": i.referral_code,
                    "Referral Code": i.referral_code,
                })
            writer.writerows(data_to_write)
        self.stdout.write(
            self.style.SUCCESS(
                f"Exported the data to {settings.BASE_DIR / os.path.join('main', 'static', 'new_data_exported.csv')}"
            ))
