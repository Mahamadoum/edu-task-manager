from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    StudentForm,
    TeacherForm,
    UserLoginForm,
    UserRegistrationForm,
)
from .models import Student, Teacher


# === AUTHENTIFICATION ===
def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Inscription réussie !")
            return redirect("home")
    else:
        form = UserRegistrationForm()
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Bienvenue {user.username} !")
                return redirect("home")
            else:
                messages.error(request, "Identifiants invalides")
        else:
            messages.error(request, "Identifiants invalides")
    else:
        form = UserLoginForm()
    return render(request, "users/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté")
    return redirect("login")


@login_required
def dashboard(request):
    context = {"user": request.user}
    if request.user.is_teacher and hasattr(request.user, "teacher_profile"):
        context["teacher"] = request.user.teacher_profile
    elif request.user.is_student and hasattr(request.user, "student_profile"):
        context["student"] = request.user.student_profile
    return render(request, "users/dashboard.html", context)


@login_required
def profile(request):
    return render(request, "users/profile.html", {"user": request.user})


# === ADMIN : GESTION DES ENSEIGNANTS ===
@login_required
@user_passes_test(lambda u: u.is_admin)
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, "admin/teachers/list.html", {"teachers": teachers})


@login_required
@user_passes_test(lambda u: u.is_admin)
def teacher_create(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Enseignant ajouté avec succès !")
            return redirect("teacher_list")
    else:
        form = TeacherForm()
    return render(
        request,
        "admin/teachers/form.html",
        {"form": form, "title": "Ajouter un enseignant"},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, "Enseignant modifié avec succès !")
            return redirect("teacher_list")
    else:
        form = TeacherForm(instance=teacher)
    return render(
        request,
        "admin/teachers/form.html",
        {"form": form, "title": "Modifier un enseignant"},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == "POST":
        teacher.user.delete()
        teacher.delete()
        messages.success(request, "Enseignant supprimé avec succès !")
        return redirect("teacher_list")
    return render(
        request, "admin/confirm_delete.html", {"object": teacher, "type": "enseignant"}
    )


# === ADMIN : GESTION DES ÉTUDIANTS ===
@login_required
@user_passes_test(lambda u: u.is_admin)
def student_list(request):
    students = Student.objects.all()
    return render(request, "admin/students/list.html", {"students": students})


@login_required
@user_passes_test(lambda u: u.is_admin)
def student_create(request):
    if request.method == "POST":
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Étudiant ajouté avec succès !")
            return redirect("student_list")
    else:
        form = StudentForm()
    return render(
        request,
        "admin/students/form.html",
        {"form": form, "title": "Ajouter un étudiant"},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Étudiant modifié avec succès !")
            return redirect("student_list")
    else:
        form = StudentForm(instance=student)
    return render(
        request,
        "admin/students/form.html",
        {"form": form, "title": "Modifier un étudiant"},
    )


@login_required
@user_passes_test(lambda u: u.is_admin)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        student.user.delete()
        student.delete()
        messages.success(request, "Étudiant supprimé avec succès !")
        return redirect("student_list")
    return render(
        request, "admin/confirm_delete.html", {"object": student, "type": "étudiant"}
    )
