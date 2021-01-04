from rest_framework import routers

from .views import MenuViewSet, OrderViewSet

router = routers.SimpleRouter()
router.register(r'guest/(?P<restaurant_id>\d+)/menu', MenuViewSet)
router.register(r'guest/(?P<restaurant_id>\d+)/order', OrderViewSet)
urlpatterns = router.urls
