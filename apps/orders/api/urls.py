from rest_framework import routers

from .views import GuestMenuViewSet, GuestOrderViewSet, GuestRestaurantViewSet

router = routers.SimpleRouter()

router.register(r'guest/restaurants', GuestRestaurantViewSet)
router.register(r'guest/(?P<restaurant_id>\d+)/menu', GuestMenuViewSet)
router.register(r'guest/(?P<restaurant_id>\d+)/order', GuestOrderViewSet)

router.register(r'owner/restaurants', GuestOrderViewSet)

urlpatterns = router.urls
