from django.db.models import Q

from rest_framework import viewsets, mixins, filters
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import GuestPermission, OwnerPermission

from apps.restaurants.models import Food, Restaurant
from apps.orders.models import Order

from .serializers import GuestFoodSerializer, GuestOrderSerializer, GuestRestaurantSerializer


class GuestBaseViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, GuestPermission)


class OwnerBaseViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, OwnerPermission)


class GuestRestaurantViewSet(mixins.ListModelMixin,
                             GuestBaseViewSet):
    """
    A simple ViewSet for listing restaurants.
    """
    queryset = Restaurant.lives.select_related('city').all()
    serializer_class = GuestRestaurantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'restaurant_type', 'seats']
    search_fields = ['name', 'city__name']
    ordering_fields = ('id', 'name', 'city', 'seats')


class GuestMenuViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GuestBaseViewSet):
    """
    A simple ViewSet for listing and retrieving restaurant menu.
    """
    queryset = Food.objects.all()
    serializer_class = GuestFoodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ('type',)
    search_fields = ['name', 'email']
    ordering_fields = ('id', 'name', 'price')

    def get_queryset(self):
        restaurant = get_object_or_404(Restaurant.lives.all(), pk=self.kwargs['restaurant_id'])

        return self.queryset.filter(
            Q(kind='') | Q(kind=restaurant.restaurant_type)
        )


class GuestOrderViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        GuestBaseViewSet):
    """
    A simple ViewSet for creating order by guest, also listing guest orders.
    """
    queryset = Order.objects.all()
    serializer_class = GuestOrderSerializer

    def get_queryset(self):
        return self.queryset.filter(
            guest=self.request.user,
            restaurant_id=self.kwargs['restaurant_id']
        )

    def perform_create(self, serializer):
        serializer.save(
            guest=self.request.user,
            # restaurant_id=self.kwargs['restaurant_id']
        )
