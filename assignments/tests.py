from datetime import datetime, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Assignment, Discipline

User = get_user_model()


class AssignmentModelTest(TestCase):
    def setUp(self):
        # Créer un utilisateur avec un profil Teacher
        self.user = User.objects.create_user(
            username="teacher",
            email="teacher@edu.fr",
            password="teacher123",
            role="teacher",
        )
        # Créer le profil Teacher manuellement
        from users.models import Teacher

        self.teacher_profile = Teacher.objects.create(user=self.user)

        self.discipline = Discipline.objects.create(
            name="Algorithmique", code="INF101", ects_credits=6
        )

    def test_create_assignment(self):
        assignment = Assignment.objects.create(
            title="Test Assignment",
            description="Test Description",
            max_score=100,
            submission_deadline=datetime.now() + timedelta(days=7),
            discipline=self.discipline,
            teacher=self.teacher_profile,  # Utiliser le profil Teacher
            is_published=True,
        )
        self.assertEqual(assignment.title, "Test Assignment")
        self.assertTrue(assignment.is_published)
