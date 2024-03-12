from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from habits.models import Habit
from users.models import User


class HabitsTestCase(APITestCase):

    def setUp(self):
        self.super_user = User.objects.create(email='superuser@test.com', is_staff=True, is_superuser=True)
        self.user = User.objects.create(email='user@test.com')
        self.client.force_authenticate(user=self.super_user)

    def test_create_habit(self):
        """Тестирование создания привычки"""
        data = {'place': 'Test', 'time': '13:00', 'action': 'test', 'time_to_complete': 100}
        response = self.client.post(reverse('habits:habit-create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.all().exists())
        self.assertEqual(response.json(),
                         {'id': 1, 'place': 'Test', 'time': '13:00:00', 'action': 'test', 'is_nice_habit': False,
                          'periodicity': 1, 'reward': None, 'time_to_complete': 100, 'is_public': False,
                          'last_message_sent': None, 'user': self.super_user.id, 'related_habit': None}
                         )

    def test_list_habit(self):
        """Тестирование вывода списка привычек"""
        habit1 = Habit.objects.create(place='list_test1', time='12:00', action='list_test1',
                                      time_to_complete=90, user=self.super_user)
        habit2 = Habit.objects.create(place='list_test2', time='12:30', action='list_test2',
                                      time_to_complete=105, user=self.user)
        response = self.client.get(reverse('habits:habit-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(habit1, Habit.objects.all())
        self.assertIn(habit2, Habit.objects.all())
        self.assertEqual(response.json(),
                         {'count': 1, 'next': None, 'previous': None, 'results':
                             [{'id': habit1.id, 'place': 'list_test1', 'time': '12:00:00', 'action': 'list_test1',
                               'is_nice_habit': False, 'periodicity': 1, 'reward': None, 'time_to_complete': 90,
                               'is_public': False, 'last_message_sent': None, 'user': self.super_user.id,
                               'related_habit': None}]}
                         )

    def test_public_list_habit(self):
        """Тестирование вывода списка публичных привычек"""
        habit3 = Habit.objects.create(place='retrieve_test1', time='22:00', action='retrieve_test1',
                                      time_to_complete=55, is_public=True)
        habit4 = Habit.objects.create(place='retrieve_test2', time='22:30', action='retrieve_test2',
                                      time_to_complete=95, is_public=False)
        response = self.client.get(reverse('habits:habit-public-get'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(habit3, Habit.objects.all())
        self.assertIn(habit4, Habit.objects.all())
        self.assertEqual(len(response.json()), 1)

    def test_update_habit(self):
        """Тестирование изменения привычки"""
        habit5 = Habit.objects.create(place='update_test', time='05:40', action='update_test',
                                      time_to_complete=115, user=self.super_user)
        update = {'place': 'update', 'time': '05:50'}
        response = self.client.patch(reverse('habits:habit-update', args=[habit5.pk]), update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(habit5, Habit.objects.all())
        self.assertEqual(response.json().get('place'), 'update')
        self.assertEqual(response.json().get('time'), '05:50:00')
        self.client.force_authenticate(user=self.user)
        update1 = {'place': 'update1', 'time': '12:50'}
        response1 = self.client.patch(reverse('habits:habit-update', args=[habit5.pk]), update1)
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_habit(self):
        """Тестирование удаления привычки"""
        habit6 = Habit.objects.create(place='delete_test', time='11:20', action='delete_test',
                                      time_to_complete=60, user=self.super_user)
        response = self.client.delete(reverse('habits:habit-delete', args=[habit6.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not Habit.objects.all().exists())
        habit7 = Habit.objects.create(place='delete_test1', time='13:25', action='delete_test1',
                                      time_to_complete=100, user=self.super_user)
        self.client.force_authenticate(user=self.user)
        response1 = self.client.delete(reverse('habits:habit-delete', args=[habit7.pk]))
        self.assertEqual(response1.status_code, status.HTTP_403_FORBIDDEN)
