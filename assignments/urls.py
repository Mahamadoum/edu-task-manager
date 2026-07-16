from django.urls import path

from . import views

app_name = "assignments"

urlpatterns = [
    # Devoirs
    path("", views.assignment_list, name="list"),
    path("<int:pk>/", views.assignment_detail, name="detail"),
    path("create/", views.assignment_create, name="create"),
    path("<int:pk>/edit/", views.assignment_edit, name="edit"),
    path("<int:pk>/delete/", views.assignment_delete, name="delete"),
    # Matières (Disciplines)
    path("disciplines/", views.discipline_list, name="discipline_list"),
    path("disciplines/create/", views.discipline_create, name="discipline_create"),
    path("disciplines/<int:pk>/edit/", views.discipline_edit, name="discipline_edit"),
    path(
        "disciplines/<int:pk>/delete/",
        views.discipline_delete,
        name="discipline_delete",
    ),
]
