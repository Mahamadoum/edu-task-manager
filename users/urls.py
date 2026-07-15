from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),
    # Admin - Teachers (préfixe dashboard/admin/)
    path("dashboard/admin/teachers/", views.teacher_list, name="teacher_list"),
    path(
        "dashboard/admin/teachers/create/", views.teacher_create, name="teacher_create"
    ),
    path(
        "dashboard/admin/teachers/<int:pk>/edit/",
        views.teacher_edit,
        name="teacher_edit",
    ),
    path(
        "dashboard/admin/teachers/<int:pk>/delete/",
        views.teacher_delete,
        name="teacher_delete",
    ),
    # Admin - Students
    path("dashboard/admin/students/", views.student_list, name="student_list"),
    path(
        "dashboard/admin/students/create/", views.student_create, name="student_create"
    ),
    path(
        "dashboard/admin/students/<int:pk>/edit/",
        views.student_edit,
        name="student_edit",
    ),
    path(
        "dashboard/admin/students/<int:pk>/delete/",
        views.student_delete,
        name="student_delete",
    ),
]
