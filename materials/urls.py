from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    SubscriptionAPIView,
    CourseViewSet,
    SubscriptionAPIView,
    LessonViewSet,
    PaymentViewSet,
    PaymentStatusAPIView,
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'payments', PaymentViewSet, basename='payment')


urlpatterns = [
    path('', include(router.urls)),
    path(
        'subscriptions/',
        SubscriptionAPIView.as_view(),
        name='subscription',
    ),
    path(
        'payments/<int:payment_id>/status/',
        PaymentStatusAPIView.as_view(),
        name='payment-status',
    ),
]