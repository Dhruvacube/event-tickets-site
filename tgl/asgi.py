import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tgl.settings")

os.environ["ASYNC_RUN"] = "True"
application = get_asgi_application()

try:
    import uwsgidecorators
    from django.core.management import call_command

    @uwsgidecorators.timer(10)
    def send_queued_mail(num):
        """Send queued mail every 10 seconds"""
        call_command("send_queued_mail", processes=1)

except ImportError:
    print("uwsgidecorators not found. Cron and timers are disabled")
