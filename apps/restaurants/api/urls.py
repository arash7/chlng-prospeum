from rest_framework import routers

from .views import RestaurantViewSet, IngredientViewSet, DishViewSet, BeverageViewSet, StockViewSet

router = routers.SimpleRouter()
router.register(r'crud/restaurants', RestaurantViewSet)
router.register(r'crud/ingredients', IngredientViewSet)
router.register(r'crud/dishes', DishViewSet)
router.register(r'crud/beverages', BeverageViewSet)
router.register(r'crud/stock', StockViewSet)
urlpatterns = router.urls
