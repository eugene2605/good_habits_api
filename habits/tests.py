from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class HabitsTestCase(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create(email='Test1', password='test1', is_staff=True, is_superuser=True)
        self.user2 = User.objects.create(email='Test2', password='test2')
        self.client.force_authenticate(user=self.user1)

    def test_create_habit(self):
        """Тестирование создания привычки"""
        data = {'place': 'Test', 'time': '13:00', 'action': 'test', 'time_to_complete': 100}
        response = self.client.post('/habit/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.all().exists())
        self.assertEqual(response.json(),
                         {'id': 1, 'place': 'Test', 'time': '13:00:00', 'action': 'test', 'is_nice_habit': False,
                          'periodicity': 1, 'reward': None, 'time_to_complete': 100, 'is_public': False,
                          'last_message_sent': None, 'user': 1, 'related_habit': None}
                         )

    def test_list_habit(self):
        """Тестирование вывода списка привычек"""
        habit1 = Habit.objects.create(place='list_test1', time='12:00', action='list_test1',
                                      time_to_complete=90, user=self.user1)
        habit2 = Habit.objects.create(place='list_test2', time='12:30', action='list_test2',
                                      time_to_complete=105, user=self.user2)
        response = self.client.get('/habit/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(habit1, Habit.objects.all())
        self.assertIn(habit2, Habit.objects.all())
        self.assertEqual(response.json(),
                         {'count': 1, 'next': None, 'previous': None, 'results':
                             [{'id': 3, 'place': 'list_test1', 'time': '12:00:00', 'action': 'list_test1',
                               'is_nice_habit': False, 'periodicity': 1, 'reward': None, 'time_to_complete': 90,
                               'is_public': False, 'last_message_sent': None, 'user': self.user1.id,
                               'related_habit': None}]}
                         )

    def test_public_list_habit(self):
        """Тестирование вывода списка публичных привычек"""
        habit3 = Habit.objects.create(place='retrieve_test1', time='22:00', action='retrieve_test1',
                                      time_to_complete=55, is_public=True)
        habit4 = Habit.objects.create(place='retrieve_test2', time='22:30', action='retrieve_test2',
                                      time_to_complete=95, is_public=False)
        response = self.client.get('/habit/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(habit3, Habit.objects.all())
        self.assertIn(habit4, Habit.objects.all())
        self.assertEqual(len(response.json()), 1)

    def test_update_habit(self):
        """Тестирование изменения привычки"""
        habit5 = Habit.objects.create(place='update_test', time='05:40', action='update_test',
                                      time_to_complete=115, user=self.user1)
        update = {'place': 'update', 'time': '05:50', 'user': self.user1.id}
        response = self.client.patch(f'/habit/update/{habit5.pk}/', update)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(habit5, Habit.objects.all())
        self.assertEqual(response.json().get('place'), 'update')
        self.assertEqual(response.json().get('time'), '05:50:00')

    def test_delete_habit(self):
        """Тестирование удаления привычки"""
        habit6 = Habit.objects.create(place='delete_test', time='11:20', action='delete_test',
                                      time_to_complete=60, user=self.user1)
        response = self.client.delete(f'/habit/delete/{habit6.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(not Habit.objects.all().exists())
