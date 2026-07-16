from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def home(request):
    return render(request, "pages/home.html")


urlpatterns = [
    path("", home, name="home"),
    path("admin/", admin.site.urls),
    path("", include("users.urls")),
    path("assignments/", include("assignments.urls")),
    path("submissions/", include("submissions.urls")),
]
