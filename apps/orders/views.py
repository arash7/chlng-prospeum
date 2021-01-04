from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import Coalesce


from apps.restaurants.models import Stock, DishIngredient
from apps.orders.models import OrderContent

from .tasks import fill_up_stock


def check_available_stock(restaurant, food, cur_order_qty):
    ordered_foods = OrderContent.objects.filter(food=food, order__restaurant=restaurant).aggregate(qty_sum=Coalesce(Sum('qty'), 0))['qty_sum']

    for di in DishIngredient.objects.filter(dish=food):
        restaurant_stock = Stock.objects.filter(
            ingredient=di.ingredient,
            restaurant=restaurant
        ).aggregate(amount_sum=Coalesce(Sum('amount'), 0))['amount_sum']
        used = di.portion * ordered_foods

        avail_stock = restaurant_stock - used
        if avail_stock < cur_order_qty * di.portion:
            fill_up_stock.delay(restaurant.id, di.ingredient_id)
            raise Exception('out of stock')

    return True
