import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tgl.settings")

os.environ["ASYNC_RUN"] = "False"
application = get_wsgi_application()
