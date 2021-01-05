from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
# from django.contrib.postgres.fields import DateTimeRangeField


class Order(models.Model):
    created_time = models.DateTimeField(_('created time'), auto_now_add=True)
    updated_time = models.DateTimeField(_('updated time'), auto_now=True)
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    restaurant = models.ForeignKey('restaurants.Restaurant', on_delete=models.PROTECT)
    reservation_date = models.DateField(_('reservation date'))
    # reservation_time = DateTimeRangeField(_('reservation time'))
    is_takeout = models.BooleanField(_('is takeout'), default=False)

    def __str__(self):
        return f'{self.restaurant_id} - {self.guest_id} - {self.reservation_date}'

    @property
    def price(self):
        return sum([oc.qty * oc.food.price for oc in OrderContent.objects.select_related('food').filter(order=self)])


class OrderContent(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='contents')
    food = models.ForeignKey('restaurants.Food', on_delete=models.PROTECT, related_name='orders')
    qty = models.PositiveIntegerField(_('quantity'))

    class Meta:
        unique_together = ('order', 'food')
