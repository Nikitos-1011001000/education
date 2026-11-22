from django.urls import path, include
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import PaymentListAPIView, UserProfileAPIView

urlpatterns = [
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