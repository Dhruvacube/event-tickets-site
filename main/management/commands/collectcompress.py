"""
 Command for deleting the resolved queries from Contact Model
"""

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "It runs collectstatic and compress command simultaneously"
    requires_system_checks = output_transaction = requires_migrations_checks = True

    def handle(self, *args, **options):
        print("Running `collectstatic` now :)\n")
        call_command("collectstatic", "--noinput")
        print("Finished running `collectstatic` \n Now running `compress` :)")
        call_command("compress", "--force")
        print("Finished....")
