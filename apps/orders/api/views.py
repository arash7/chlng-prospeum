from rest_framework import viewsets, mixins, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from .permissions import GuestPermission, OwnerPermission

from apps.restaurants.models import Food
from apps.orders.models import Order

from .serializers import FoodSerializer, OrderSerializer


class GuestBaseViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, GuestPermission)


class OwnerBaseViewSet(viewsets.GenericViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, OwnerPermission)


class MenuViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  GuestBaseViewSet):
    """
    A simple ViewSet for listing and retrieving restaurant menu.
    """
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['restaurant', 'type']
    search_fields = ['name', 'email']
    ordering_fields = ('id', 'name', 'price')

    def get_queryset(self):
        return self.queryset.filter(restaurant_id=self.kwargs['restaurant_id'])


class OrderViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   GuestBaseViewSet):
    """
    A simple ViewSet for creating order by guest, also listing guest orders.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(
            guest=self.request.user,
            restaurant_id=self.kwargs['restaurant_id']
        )

    def perform_create(self, serializer):
        serializer.save(
            guest=self.request.user,
            restaurant_id=self.kwargs['restaurant_id']
        )
