import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from users.models import User, Teacher, Student

def create_users():
    # Admin
    admin, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@edu.fr',
            'password': 'admin123',
            'first_name': 'Admin',
            'last_name': 'System',
            'role': 'admin',
            'is_verified': True
        }
    )
    if created:
        admin.set_password('admin123')
        admin.save()
        print('✅ Admin créé: admin / admin123')
    else:
        print('ℹ️ Admin existe déjà')

    # Enseignant
    teacher_user, created = User.objects.get_or_create(
        username='teacher',
        defaults={
            'email': 'teacher@edu.fr',
            'password': 'teacher123',
            'first_name': 'Professeur',
            'last_name': 'Test',
            'role': 'teacher',
            'is_verified': True
        }
    )
    if created:
        teacher_user.set_password('teacher123')
        teacher_user.save()
        Teacher.objects.get_or_create(
            user=teacher_user,
            defaults={
                'department': 'Informatique',
                'office_location': 'Bureau 101',
                'consultation_hours': 'Lundi 14h-16h'
            }
        )
        print('✅ Enseignant créé: teacher / teacher123')
    else:
        print('ℹ️ Enseignant existe déjà')

    # Étudiant
    student_user, created = User.objects.get_or_create(
        username='student',
        defaults={
            'email': 'student@edu.fr',
            'password': 'student123',
            'first_name': 'Étudiant',
            'last_name': 'Test',
            'role': 'student',
            'is_verified': True
        }
    )
    if created:
        student_user.set_password('student123')
        student_user.save()
        Student.objects.get_or_create(
            user=student_user,
            defaults={
                'student_id': 'STU2025001',
                'level': 'M1',
                'group_code': 'INFO-A',
                'enrolled_year': 2025
            }
        )
        print('✅ Étudiant créé: student / student123')
    else:
        print('ℹ️ Étudiant existe déjà')

    print('\n=== COMPTES DE TEST ===')
    print('Admin    : admin / admin123')
    print('Enseignant: teacher / teacher123')
    print('Étudiant : student / student123')

if __name__ == '__main__':
    create_users()
