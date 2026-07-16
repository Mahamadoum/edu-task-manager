from django.urls import path
from . import views

app_name = 'submissions'

urlpatterns = [
    path('create/<int:assignment_pk>/', views.submission_create, name='create'),
    path('grade/<int:submission_pk>/', views.grade_create, name='grade'),
]
