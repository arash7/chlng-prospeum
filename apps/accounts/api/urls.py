from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('v1/token/obtain/', TokenObtainPairView.as_view(), name="obtain-token"),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name="refresh-token"),
]
