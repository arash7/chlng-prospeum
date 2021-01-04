from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions

from apps.restaurants.models import Food
from apps.orders.models import Order, OrderContent


class FoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = ('id', 'name', 'price', 'type')


class OrderContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderContent
        exclude = ('order',)


class OrderSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(read_only=True)
    contents = OrderContentSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = '__all__'
        extra_kwargs = {
            'restaurant': {'read_only': True},
            'guest': {'read_only': True}
        }

    def validate(self, attrs):
        for c in attrs['contents']:
            if c.food.restaurant_id != self.context['kwargs']['restaurant_id']:
                raise exceptions.ParseError(_('this restaurant does not server {}'))
        return attrs

    def create(self, validated_data):
        contents = validated_data.pop('contents')
        instance = super().create(validated_data)
        OrderContent.objects.bulk_create([OrderContent(order=instance, **content) for content in contents])
        return instance
