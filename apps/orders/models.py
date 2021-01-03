from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import DateTimeRangeField


class Order(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.PROTECT)
    reservation_time = DateTimeRangeField(_('reservation time'))
    reservation_date = models.DateField(_('reservation date'))
    is_takeout = models.BooleanField(_('is takeout'), default=False)

    content = models.ManyToManyField('restaurants.Food', through='OrderContent', blank=False)


class OrderContent(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food = models.ForeignKey('restaurants.Food', on_delete=models.PROTECT)
    qty = models.PositiveIntegerField(_('quantity'))

    class Meta:
        unique_together = ('order', 'food')
