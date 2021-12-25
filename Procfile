web: gunicorn tgl.asgi:application -k tgl.workers.DynamicUvicornWorker --timeout 500
worker: celery -A tgl worker -B -Q celery -l info -E --without-gossip --without-mingle --without-heartbeat