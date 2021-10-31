from tgl.celery import app

from post_office.mail import send_queued_mail_until_done

@app.task
def mail_queue():
    send_queued_mail_until_done()