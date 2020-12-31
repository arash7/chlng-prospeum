from rest_framework import routers

from .views import RestaurantViewSet, IngredientViewSet, DishViewSet, BeverageViewSet

router = routers.SimpleRouter()
router.register(r'v1/crud/restaurants', RestaurantViewSet)
router.register(r'v1/crud/ingredients', IngredientViewSet)
router.register(r'v1/crud/dishes', DishViewSet)
router.register(r'v1/crud/beverages', BeverageViewSet)
urlpatterns = router.urls
