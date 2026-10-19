from django.urls import path

from .views import PaymentListAPIView, UserProfileAPIView

urlpatterns = [
    # существующие маршруты ...
    path(
        "payments/",
        PaymentListAPIView.as_view(),
        name="payment-list",
    ),
    path(
        "users/<int:pk>/",
        UserProfileAPIView.as_view(),
        name="user-profile",
    ),
]