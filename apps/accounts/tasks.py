import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task()
def send_fake_mail(email, message):
    logger.info(f'email sent to {email}, message: {message}')
