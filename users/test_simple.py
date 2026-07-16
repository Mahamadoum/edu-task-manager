from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class SimpleTest(TestCase):
    def test_math(self):
        self.assertEqual(1 + 1, 2)

    def test_user_creation(self):
        user = User.objects.create_user(
            username='testuser',
            email='test@test.com',
            password='test123'
        )
        self.assertEqual(user.username, 'testuser')
