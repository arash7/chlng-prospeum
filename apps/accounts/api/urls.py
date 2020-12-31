from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/obtain/', TokenObtainPairView.as_view(), name="obtain-token"),
    path('token/refresh/', TokenRefreshView.as_view(), name="refresh-token"),
]
