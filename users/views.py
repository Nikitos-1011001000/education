from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated

from .filters import PaymentFilter
from .models import Payment, User
from .serializers import (
    PaymentSerializer,
    UserProfileSerializer,
    OwnProfileSerializer,
    PublicProfileSerializer,
)
from .permissions import IsOwnerOrReadOnly

class IsProfileOwner(permissions.BasePermission):
    """
    Редактировать профиль может только его владелец.
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """

    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_serializer_class(self):
        profile_id = self.kwargs.get('pk')

        if self.request.user.pk == profile_id:
            return OwnProfileSerializer

        return PublicProfileSerializer

class PaymentListAPIView(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter

class UserProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsProfileOwner]

    def get_serializer_class(self):
        profile_id = self.kwargs.get('pk')

        if self.request.user.pk == profile_id:
            return OwnProfileSerializer

        return PublicProfileSerializer

class MyPaymentsAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)
