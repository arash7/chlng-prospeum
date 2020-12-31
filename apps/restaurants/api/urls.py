from rest_framework import routers

from .views import RestaurantViewSet, IngredientViewSet, DishViewSet, BeverageViewSet

router = routers.SimpleRouter()
router.register(r'crud/restaurants', RestaurantViewSet)
router.register(r'crud/ingredients', IngredientViewSet)
router.register(r'crud/dishes', DishViewSet)
router.register(r'crud/beverages', BeverageViewSet)
urlpatterns = router.urls
