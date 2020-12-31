from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions

from ..models import Restaurant, Ingredient, Dish, Beverage


class RestaurantSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class DishSerializer(serializers.ModelSerializer):

    class Meta:
        model = Dish
        exclude = ('type', 'price')


class BeverageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Beverage
        exclude = ('type', 'ingredients')
        extra_kwargs = {
            "price": {"required": True},
        }

    def validate_price(self, value):
        if value <= 0:
            raise exceptions.ParseError(_('price is invalid!'))
        return value
