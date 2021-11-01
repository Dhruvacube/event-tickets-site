import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tgl.settings")

os.environ["ASYNC_RUN"] = "True"
application = get_asgi_application()
