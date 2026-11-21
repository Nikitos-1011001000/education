from django.contrib.auth.models import Group
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class LessonCRUDTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            email='owner@example.com',
            password='StrongPass123!',
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='StrongPass123!',
        )
        self.moderator = User.objects.create_user(
            email='moderator@example.com',
            password='StrongPass123!',
        )

        moderator_group, _ = Group.objects.get_or_create(name='moderator')
        self.moderator.groups.add(moderator_group)

        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Курс для тестов',
            owner=self.owner,
        )

        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание урока',
            course=self.course,
            owner=self.owner,
        )

        self.list_url = reverse('lesson-list')
        self.detail_url = reverse('lesson-detail', args=[self.lesson.id])

    def test_owner_can_create_lesson(self):
        self.client.force_authenticate(user=self.owner)

        data = {
            'title': 'Новый урок',
            'description': 'Новое описание',
            'course': self.course.id,
        }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(
            Lesson.objects.count(),
            2,
        )
        self.assertEqual(
            Lesson.objects.last().owner,
            self.owner,
        )

    def test_unauthenticated_user_cannot_create_lesson(self):
        data = {
            'title': 'Новый урок',
            'description': 'Новое описание',
            'course': self.course.id,
        }

        response = self.client.post(self.list_url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(
            Lesson.objects.count(),
            1,
        )

    def test_owner_can_retrieve_own_lesson(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['title'],
            'Тестовый урок',
        )

    def test_other_user_cannot_retrieve_foreign_lesson(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_moderator_can_retrieve_any_lesson(self):
        self.client.force_authenticate(user=self.moderator)

        response = self.client.get(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['title'],
            'Тестовый урок',
        )

    def test_owner_can_update_own_lesson(self):
        self.client.force_authenticate(user=self.owner)

        data = {
            'title': 'Обновлённый урок',
            'description': 'Обновлённое описание',
            'course': self.course.id,
        }

        response = self.client.patch(self.detail_url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.lesson.refresh_from_db()
        self.assertEqual(
            self.lesson.title,
            'Обновлённый урок',
        )

    def test_other_user_cannot_update_foreign_lesson(self):
        self.client.force_authenticate(user=self.other_user)

        data = {
            'title': 'Попытка изменения',
        }

        response = self.client.patch(self.detail_url, data, format='json')

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.lesson.refresh_from_db()
        self.assertEqual(
            self.lesson.title,
            'Тестовый урок',
        )

    def test_owner_can_delete_own_lesson(self):
        self.client.force_authenticate(user=self.owner)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Lesson.objects.filter(id=self.lesson.id).exists(),
        )

    def test_other_user_cannot_delete_foreign_lesson(self):
        self.client.force_authenticate(user=self.other_user)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )
        self.assertTrue(
            Lesson.objects.filter(id=self.lesson.id).exists(),
        )


class SubscriptionTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='user@example.com',
            password='StrongPass123!',
        )
        self.other_user = User.objects.create_user(
            email='other@example.com',
            password='StrongPass123!',
        )

        self.course = Course.objects.create(
            title='Курс по немецкому',
            description='Базовый курс',
            owner=self.other_user,
        )

        self.subscription_url = reverse('subscription')
        self.course_list_url = reverse('course-list')

    def test_user_can_subscribe_to_course(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.id},
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['message'],
            'подписка добавлена',
        )
        self.assertTrue(
            Subscription.objects.filter(
                user=self.user,
                course=self.course,
            ).exists(),
        )

    def test_user_can_unsubscribe_from_course(self):
        Subscription.objects.create(
            user=self.user,
            course=self.course,
        )

        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.id},
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            response.data['message'],
            'подписка удалена',
        )
        self.assertFalse(
            Subscription.objects.filter(
                user=self.user,
                course=self.course,
            ).exists(),
        )

    def test_subscription_toggles_on_repeated_request(self):
        self.client.force_authenticate(user=self.user)

        first_response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.id},
            format='json',
        )
        second_response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.id},
            format='json',
        )

        self.assertEqual(
            first_response.data['message'],
            'подписка добавлена',
        )
        self.assertEqual(
            second_response.data['message'],
            'подписка удалена',
        )
        self.assertEqual(
            Subscription.objects.count(),
            0,
        )

    def test_unauthenticated_user_cannot_subscribe(self):
        response = self.client.post(
            self.subscription_url,
            {'course_id': self.course.id},
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(
            Subscription.objects.count(),
            0,
        )

    def test_subscription_requires_course_id(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.subscription_url,
            {},
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertEqual(
            response.data['error'],
            'Не передан course_id',
        )

    def test_subscription_for_nonexistent_course(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.post(
            self.subscription_url,
            {'course_id': 999999},
            format='json',
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_course_response_contains_subscription_flag(self):
        self.client.force_authenticate(user=self.user)

        response = self.client.get(self.course_list_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertFalse(
            response.data['results'][0]['is_subscribed'],
        )

        self.client.post(
            self.subscription_url,
            {'course_id': self.course.id},
            format='json',
        )

        response = self.client.get(self.course_list_url)

        self.assertTrue(
            response.data['results'][0]['is_subscribed'],
        )
