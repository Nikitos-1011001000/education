from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import PaymentListAPIView, UserProfileAPIView

urlpatterns = [
    # существующие маршруты ...
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "users/<int:pk>/",
        views.UserProfileAPIView.as_view(),
        name="user-detail",
    ),
    path(
        'payments/',
        views.MyPaymentsAPIView.as_view(),
        name='my-payments',
    ),
]