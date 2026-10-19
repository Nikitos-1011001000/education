from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from .filters import PaymentFilter
from .models import Payment, User
from .serializers import PaymentSerializer, UserProfileSerializer


class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

class UserProfileAPIView(generics.RetrieveAPIView):
    queryset = User.objects.prefetch_related("payments")
    serializer_class = UserProfileSerializer
