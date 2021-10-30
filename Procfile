web: gunicorn tgl.asgi:application -k tgl.workers.DynamicUvicornWorker --timeout 500
worker: celery -A tgl worker  -l info -E