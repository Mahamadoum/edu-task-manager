from django.db import models
from django.conf import settings

class Discipline(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    ects_credits = models.IntegerField(default=0)
    semester = models.CharField(max_length=10, blank=True)
    teacher = models.ForeignKey('users.Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='disciplines')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

class Assignment(models.Model):
    class Type(models.TextChoices):
        HOMEWORK = 'homework', 'Devoir'
        EXAM = 'exam', 'Examen'
        PROJECT = 'project', 'Projet'
        QUIZ = 'quiz', 'Quiz'
        LAB = 'lab', 'TP'

    class Difficulty(models.TextChoices):
        BEGINNER = 'beginner', 'Débutant'
        INTERMEDIATE = 'intermediate', 'Intermédiaire'
        ADVANCED = 'advanced', 'Avancé'
        EXPERT = 'expert', 'Expert'

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    assignment_type = models.CharField(max_length=20, choices=Type.choices, default=Type.HOMEWORK)
    difficulty_level = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.INTERMEDIATE)
    max_score = models.IntegerField(default=100)
    passing_score = models.IntegerField(default=50)
    submission_deadline = models.DateTimeField()
    estimated_duration = models.IntegerField(default=60)
    is_mandatory = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    instructions = models.TextField(blank=True)
    attachments = models.JSONField(default=list, blank=True)
    discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE, related_name='assignments')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, related_name='assignments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

def submission_file_path(instance, filename):
    return f'submissions/{instance.student.user.username}/{instance.assignment.id}/{filename}'

class Submission(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Brouillon'
        SUBMITTED = 'submitted', 'Soumis'
        GRADED = 'graded', 'Noté'
        RETURNED = 'returned', 'Retourné'

    content = models.TextField(blank=True)
    file = models.FileField(upload_to=submission_file_path, null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_late = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    plagiarism_score = models.FloatField(default=0.0)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey('users.Student', on_delete=models.CASCADE, related_name='submissions')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.assignment.title}"

class Grade(models.Model):
    score = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)
    graded_at = models.DateTimeField(auto_now_add=True)
    is_final = models.BooleanField(default=False)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, related_name='grade')
    teacher = models.ForeignKey('users.Teacher', on_delete=models.CASCADE, related_name='grades')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.submission} - {self.score}"