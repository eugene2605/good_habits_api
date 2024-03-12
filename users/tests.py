from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UsersTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='admin@test.ru', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """Тестирование создания пользователя"""
        data = {'email': 'test@mail.ru', 'password': 'test'}
        response = self.client.post(reverse('users:user_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.all().exists())

    def test_update_user(self):
        """Тестирование изменения пользователя"""
        update = {'email': 'test@test.ru'}
        response = self.client.patch(reverse('users:user_update', args=[self.user.pk]), update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user, User.objects.all())
        self.assertEqual(response.json().get('email'), 'test@test.ru')
