from __future__ import absolute_import

import os

from celery import Celery, shared_task
from celery.schedules import crontab
from django.conf import settings
from django.core.management import call_command

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tgl.settings")

app = Celery("tgl", broker_url=settings.BROKER_URL)
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def mail_queue():
    call_command("send_queued_mail", processes=1)
