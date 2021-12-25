"""
 It gets all those users data who haven't made any payment, failed or pending
"""

import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from accounts.models import User


class Command(BaseCommand):
    help = (
        "It gets all those users data who haven't made any payment, failed or pending"
    )
    requires_system_checks = output_transaction = requires_migrations_checks = True

    def handle(self, *args, **options):
        try:
            users_iterator1 = User.objects.filter(
                orders__payment_status__in=["P", "F"],
                is_staff=False).values("first_name", "last_name",
                                       "university_name", "phone")
            users_iterator2 = User.objects.filter(
                orders=None, is_staff=False).values("first_name", "last_name",
                                                    "university_name", "phone")
            dump_data = [{
                "First Name": i.get("first_name"),
                "Last Name": i.get("last_name"),
                "University": i.get("university_name"),
                "Phone": i.get("phone"),
            } for i in users_iterator1.union(users_iterator2).iterator()]
            new_data_csv_file_path = settings.BASE_DIR / os.path.join(
                "main", "static", "new_data_generated_failed_users.csv")
            with open(new_data_csv_file_path, "w") as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=[
                        "First Name", "Last Name", "University", "Phone"
                    ],
                )
                writer.writeheader()
                writer.writerows(dump_data)
            self.stdout.write(self.style.SUCCESS("Success"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
