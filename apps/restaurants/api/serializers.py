from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions

from ..models import Restaurant, Ingredient, DishIngredient, Dish, Beverage, Stock


class RestaurantSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class DishIngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = DishIngredient
        exclude = ('dish',)


class DishSerializer(serializers.ModelSerializer):
    ingredients = DishIngredientSerializer(many=True)

    class Meta:
        model = Dish
        exclude = ('type', 'price')

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().create(validated_data)
        DishIngredient.objects.bulk_create([DishIngredient(dish=instance, **ingredient) for ingredient in ingredients])
        return instance

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance = super().update(instance, validated_data)
        if ingredients:
            instance.ingredients.clear()
            DishIngredient.objects.bulk_create([DishIngredient(dish=instance, **ingredient) for ingredient in ingredients])
        return instance


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


class StockSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stock
        fields = '__all__'
