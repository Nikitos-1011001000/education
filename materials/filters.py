import django_filters

from .models import Payment


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = ['payment_method', 'status', 'paid_course']