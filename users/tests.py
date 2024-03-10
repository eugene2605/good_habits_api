from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UsersTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='Admin', password='admin', is_staff=True, is_superuser=True)
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """Тестирование создания пользователя"""
        data = {'email': 'Test@mail.ru', 'password': 'Test'}
        response = self.client.post('/user/registr/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.all().exists())

    def test_update_user(self):
        """Тестирование изменения пользователя"""
        update = {'password': 'Update'}
        response = self.client.patch(f'/user/update/{self.user.pk}/', update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(self.user, User.objects.all())
        self.assertEqual(response.json().get('password'), 'Update')
