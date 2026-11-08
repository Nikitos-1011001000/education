from rest_framework import viewsets, generics, permissions, status
from rest_framework.permissions import IsAuthenticated

from .models import Course, Lesson, Subscription, Payment
from .serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer, PaymentSerializer, SubscriptionRequestSerializer
from .permissions import IsOwner, IsOwnerOrModerator
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from materials.paginators import StandardPagination
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
)
from materials.services import (
    create_payment_session,
    retrieve_stripe_session,
)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        course = serializer.validated_data['paid_course']

        stripe_data = create_payment_session(course)

        serializer.save(
            user=self.request.user,
            amount=course.price,
            payment_method='transfer',
            stripe_session_id=stripe_data['stripe_session_id'],
            payment_url=stripe_data['payment_url'],
        )

class PaymentStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, payment_id):
        payment = Payment.objects.filter(
            id=payment_id,
            user=request.user,
        ).first()

        if payment is None:
            return Response(
                {'error': 'Платёж не найден'},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not payment.stripe_session_id:
            return Response(
                {'error': 'Для платежа не создана Stripe-сессия'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        session_data = retrieve_stripe_session(
            payment.stripe_session_id,
        )

        return Response(session_data)

class SubscriptionAPIView(APIView):
    @extend_schema(
        summary='Подписаться или отписаться от курса',
        description=(
                'Переключает подписку текущего пользователя на курс. '
                'Если подписки нет — создаёт её, если есть — удаляет.'
        ),
        request=SubscriptionRequestSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {
                        'type': 'string',
                        'example': 'подписка добавлена',
                    }
                },
            },
            400: {
                'description': 'Не передан course_id.',
            },
            401: {
                'description': 'Пользователь не авторизован.',
            },
            404: {
                'description': 'Курс не найден.',
            },
        },
        examples=[
            OpenApiExample(
                'Пример запроса',
                value={'course_id': 5},
            ),
            OpenApiExample(
                'Подписка добавлена',
                value={'message': 'подписка добавлена'},
                response_only=True,
            ),
            OpenApiExample(
                'Подписка удалена',
                value={'message': 'подписка удалена'},
                response_only=True,
            ),
        ],
    )

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get('course_id')

        if course_id is None:
            return Response(
                {'error': 'Не передан course_id'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        course_item = get_object_or_404(Course, id=course_id)

        subs_item = Subscription.objects.filter(
            user=user,
            course=course_item,
        )

        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        else:
            Subscription.objects.create(
                user=user,
                course=course_item,
            )
            message = 'подписка добавлена'

        return Response({'message': message})

def is_moderator(user):
    """
    Проверяет, состоит ли пользователь в группе модераторов.
    """
    return (
        user.is_authenticated
        and user.groups.filter(name='moderator').exists()
    )


class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD для курсов.

    Обычный пользователь работает только со своими курсами.
    Модератор видит и может редактировать все курсы,
    но удалять может только свои.
    """
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = StandardPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Course.objects.all()

        if self.action in ('update', 'partial_update', 'destroy'):
            if not is_moderator(self.request.user):
                return queryset.filter(owner=self.request.user)

        return queryset


    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]

        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]

        else:
            permission_classes = [IsAuthenticated]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = StandardPagination

class LessonViewSet(viewsets.ModelViewSet):
    """
    CRUD для уроков.

    Обычный пользователь работает только со своими уроками.
    Модератор видит и может редактировать все уроки,
    но удалять может только свои.
    """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Lesson.objects.all()

        if is_moderator(self.request.user):
            return queryset

        return queryset.filter(owner=self.request.user)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]

        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsOwnerOrModerator]

        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]

        else:
            permission_classes = [IsAuthenticated]

        return [
            permission()
            for permission in permission_classes
        ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class LessonCreateAPIView(APIView):  # или ListCreateAPIView и т.д.
    pass

class LessonDestroyAPIView(APIView):
    pass

class LessonListAPIView(APIView):
    pass

class LessonRetrieveAPIView(APIView):
    pass

class LessonUpdateAPIView(APIView):
    pass

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer