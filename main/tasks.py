from post_office.mail import send_queued_mail_until_done

from tgl.celery import app


@app.task
def mail_queue():
    send_queued_mail_until_done()
