from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrateur"
        TEACHER = "teacher", "Enseignant"
        STUDENT = "student", "Étudiant"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT


class Teacher(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="teacher_profile"
    )
    department = models.CharField(max_length=100, blank=True)
    office_location = models.CharField(max_length=200, blank=True)
    consultation_hours = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Prof. {self.user.get_full_name()}"


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    student_id = models.CharField(max_length=20, unique=True)
    group_code = models.CharField(max_length=20, blank=True)
    level = models.CharField(max_length=10, blank=True)
    enrolled_year = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"
