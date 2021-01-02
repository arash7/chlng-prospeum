from celery import shared_task

from .models import DishIngredient, Food


@shared_task()
def calc_dish_price(dish_id):
    ing_list = DishIngredient.objects.select_related('ingredient').filter(dish_id=dish_id)
    dish_price = sum([i.portion * i.ingredient.price for i in ing_list])
    Food.objects.filter(pk=dish_id).update(price=dish_price)