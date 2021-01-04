from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from ..models import Restaurant, Ingredient, Dish, Beverage, Stock
from .serializers import RestaurantSerializer, IngredientSerializer, DishSerializer, BeverageSerializer, StockSerializer


class BaseCRUD(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAdminUser, DjangoModelPermissions)


class RestaurantViewSet(BaseCRUD):
    """
    A simple ViewSet for Restaurant CRUD operations.
    """
    queryset = Restaurant.objects.select_related('city').all()
    serializer_class = RestaurantSerializer

    # def perform_create(self, serializer):
    #     serializer.save(owner=self.request.user)


class IngredientViewSet(BaseCRUD):
    """
    A simple ViewSet for Ingredient CRUD operations.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class DishViewSet(BaseCRUD):
    """
    A simple ViewSet for Dish CRUD operations.
    """
    queryset = Dish.objects.filter(type=Dish.TYPE_DISH)
    serializer_class = DishSerializer


class BeverageViewSet(BaseCRUD):
    """
    A simple ViewSet for Beverage CRUD operations.
    """
    queryset = Beverage.objects.filter(type=Dish.TYPE_BEVERAGE)
    serializer_class = BeverageSerializer


class StockViewSet(BaseCRUD):
    """
    A simple ViewSet for Stock CRUD operations.
    """
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
