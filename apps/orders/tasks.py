import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task()
def fill_up_stock(ingredient_id, restaurant_id):
    logger.critical(f'restaurant {restaurant_id} needs ingredient {ingredient_id}')
