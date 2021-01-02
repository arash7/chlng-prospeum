from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Dish
from .tasks import calc_dish_price


@receiver(post_save, sender=Dish)
def dish_cal_price(sender, instance, created, **kwargs):
    calc_dish_price.apply_async(args=[instance.id], countdown=3)

