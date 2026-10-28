from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer
from rest_framework import serializers

from .models import Payment, User

class PublicProfileSerializer(serializers.ModelSerializer):
    """
    Общая информация о любом пользователе.
    Не содержит пароль, фамилию и историю платежей.
    """

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'avatar',
        ]
        read_only_fields = fields


class OwnProfileSerializer(serializers.ModelSerializer):
    """
    Полный профиль для самого пользователя.
    Пароль никогда не возвращается.
    """

    password = serializers.CharField(
        write_only=True,
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'avatar',
            'password',
        ]
        read_only_fields = [
            'id',
            'username',
        ]

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)

        for attribute, value in validated_data.items():
            setattr(instance, attribute, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"

class UserRegistrationSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        # Только то, что нужно при создании. Пароль — обязательно, остальное — по модели
        fields = ['email', 'password', 'username', 'phone', 'city', 'avatar']
        extra_kwargs = {
            'password': {'write_only': True},  # не отдаём пароль в ответе
            'avatar': {'required': False},     # аватарка необязательна    # если username обязателен в модели
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # хешируем пароль через Django
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'username',
            'avatar',
            'city',
            'phone',
            'payments',
        ]  # без пароля, фамилии (если first_name — имя), истории платежей
        read_only_fields = [
            'email',
            'payments',
        ]