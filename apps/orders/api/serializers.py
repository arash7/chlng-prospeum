from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers, exceptions

from apps.restaurants.models import Food, Restaurant
from apps.orders.models import Order, OrderContent


class GuestRestaurantSerializer(serializers.ModelSerializer):
    city_name = serializers.CharField(source='city.name', read_only=True)

    class Meta:
        model = Restaurant
        fields = ('id', 'name', 'restaurant_type', 'city_name', 'seats')


class GuestFoodSerializer(serializers.ModelSerializer):

    class Meta:
        model = Food
        fields = ('id', 'name', 'price', 'type')


class GuestOrderContentSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderContent
        exclude = ('id', 'order')


class GuestOrderSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(read_only=True)
    contents = GuestOrderContentSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        exclude = ('guest',)
        extra_kwargs = {
            'restaurant': {'read_only': True},
        }

    def validate_reservation_date(self, value):
        if value < timezone.now().date():
            raise exceptions.ParseError(_(f'date {value} can not be reserved'))
        return value

    def validate(self, attrs):
        try:
            restaurant = Restaurant.lives.get(pk=self.context['view'].kwargs['restaurant_id'])
        except Restaurant.DoesNotExist:
            raise exceptions.NotFound(_('restaurant not available'))

        if restaurant.seats == 0 and not attrs.get('is_takeout', False):
            raise exceptions.NotFound(_('restaurant only excepts takeout orders'))

        for c in attrs['contents']:
            if c['food'].kind != '' and c['food'].kind != restaurant.restaurant_type:
                print(c['food'].kind, restaurant.restaurant_type)
                raise exceptions.ParseError(_(f'this restaurant does not server `{c["food"].name}`'))

        attrs['restaurant'] = restaurant
        return attrs

    def create(self, validated_data):
        contents = validated_data.pop('contents')
        instance = super().create(validated_data)
        OrderContent.objects.bulk_create([OrderContent(order=instance, **content) for content in contents])
        return instance
