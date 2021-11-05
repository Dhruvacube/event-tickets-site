"""
 Command for mailing all the data
"""

import csv

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand
from post_office import mail

from accounts.models import *
from announcements.models import *
from main.models import *
from payments.models import *
from referral.models import *


class Command(BaseCommand):
    help = " Command for mailing all the data"
    requires_system_checks = output_transaction = True

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument("poll_ids", nargs="+", type=int)

        # Named (optional) arguments
        parser.add_argument(
            "--delete",
            action="store_true",
            help="Delete poll instead of closing it",
        )

    def handle(self, *args, **options):
        call_command("collectstatic", "--noinput")
        self.stdout.write(
            self.style.SUCCESS(
                "Finished running `collectstatic` \n Now running `compress` :)"
            ))
        call_command("compress", "--force")
        self.stdout.write(self.style.SUCCESS("Finished...."))
