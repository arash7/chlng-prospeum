from celery import shared_task


@shared_task()
def send_fake_mail(email, message):
    print(f'email sent to {email}')
    print(message)
