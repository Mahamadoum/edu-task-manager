from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
)

from .models import Student, Teacher, User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=User.Role.choices, initial=User.Role.STUDENT)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "password1",
            "password2",
        ]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name", "role", "is_active"]


class TeacherForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    department = forms.CharField(max_length=100, required=False)
    office_location = forms.CharField(max_length=200, required=False)
    consultation_hours = forms.CharField(max_length=200, required=False)

    class Meta:
        model = Teacher
        fields = ["department", "office_location", "consultation_hours"]

    def save(self, commit=True):
        user_data = {
            "username": self.cleaned_data["username"],
            "email": self.cleaned_data["email"],
            "first_name": self.cleaned_data["first_name"],
            "last_name": self.cleaned_data["last_name"],
            "role": User.Role.TEACHER,
        }
        if self.cleaned_data.get("password"):
            user_data["password"] = self.cleaned_data["password"]

        if self.instance.pk:
            user = self.instance.user
            for key, value in user_data.items():
                if key != "password":
                    setattr(user, key, value)
                elif value:
                    user.set_password(value)
            user.save()
        else:
            user = User.objects.create_user(**user_data)
            self.instance.user = user
        return super().save(commit)


class StudentForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    student_id = forms.CharField(max_length=20)
    group_code = forms.CharField(max_length=20, required=False)
    level = forms.CharField(max_length=10, required=False)
    enrolled_year = forms.IntegerField(required=False)

    class Meta:
        model = Student
        fields = ["student_id", "group_code", "level", "enrolled_year"]

    def save(self, commit=True):
        user_data = {
            "username": self.cleaned_data["username"],
            "email": self.cleaned_data["email"],
            "first_name": self.cleaned_data["first_name"],
            "last_name": self.cleaned_data["last_name"],
            "role": User.Role.STUDENT,
        }
        if self.cleaned_data.get("password"):
            user_data["password"] = self.cleaned_data["password"]

        if self.instance.pk:
            user = self.instance.user
            for key, value in user_data.items():
                if key != "password":
                    setattr(user, key, value)
                elif value:
                    user.set_password(value)
            user.save()
        else:
            user = User.objects.create_user(**user_data)
            self.instance.user = user
        return super().save(commit)
