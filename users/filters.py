from django_filters import rest_framework as filters

from .models import Payment


class PaymentFilter(filters.FilterSet):
    payment_date = filters.OrderingFilter(
        fields=["payment_date"],
        label="Сортировка по дате оплаты",
    )
    paid_course = filters.NumberFilter(
        field_name="paid_course",
        label="ID курса",
    )
    paid_lesson = filters.NumberFilter(
        field_name="paid_lesson",
        label="ID урока",
    )
    payment_method = filters.ChoiceFilter(
        choices=Payment.PAYMENT_METHOD_CHOICES,
        label="Способ оплаты",
    )

    class Meta:
        model = Payment
        fields = [
            "paid_course",
            "paid_lesson",
            "payment_method",
        ]