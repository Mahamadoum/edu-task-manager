from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            username="testuser", email="test@edu.fr", password="test123", role="student"
        )
        self.assertEqual(user.username, "testuser")
        self.assertTrue(user.is_student)
        self.assertFalse(user.is_teacher)
        self.assertFalse(user.is_admin)

    def test_create_teacher(self):
        user = User.objects.create_user(
            username="teacher1",
            email="teacher@edu.fr",
            password="teacher123",
            role="teacher",
        )
        self.assertTrue(user.is_teacher)
        self.assertFalse(user.is_student)

    def test_create_admin(self):
        user = User.objects.create_user(
            username="admin1", email="admin@edu.fr", password="admin123", role="admin"
        )
        self.assertTrue(user.is_admin)
