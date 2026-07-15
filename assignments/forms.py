from django import forms

from .models import Assignment, Discipline, Grade, Submission


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = [
            "title",
            "description",
            "assignment_type",
            "difficulty_level",
            "max_score",
            "passing_score",
            "submission_deadline",
            "estimated_duration",
            "is_mandatory",
            "is_published",
            "instructions",
            "discipline",
        ]
        widgets = {
            "submission_deadline": forms.DateTimeInput(
                attrs={"type": "datetime-local", "class": "form-control"}
            ),
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "instructions": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "assignment_type": forms.Select(attrs={"class": "form-control"}),
            "difficulty_level": forms.Select(attrs={"class": "form-control"}),
            "max_score": forms.NumberInput(attrs={"class": "form-control"}),
            "passing_score": forms.NumberInput(attrs={"class": "form-control"}),
            "estimated_duration": forms.NumberInput(attrs={"class": "form-control"}),
            "discipline": forms.Select(attrs={"class": "form-control"}),
        }
        labels = {
            "title": "Titre du devoir",
            "description": "Description",
            "assignment_type": "Type de devoir",
            "difficulty_level": "Niveau de difficulté",
            "max_score": "Note maximale",
            "passing_score": "Note de passage",
            "submission_deadline": "Date limite de rendu",
            "estimated_duration": "Durée estimée (minutes)",
            "is_mandatory": "Obligatoire",
            "is_published": "Publier le devoir",
            "instructions": "Instructions",
            "discipline": "Matière",
        }


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ["content", "file"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "rows": 6,
                    "class": "form-control",
                    "placeholder": "Écrivez votre réponse ici...",
                }
            ),
            "file": forms.FileInput(attrs={"class": "form-control"}),
        }
        labels = {
            "content": "Contenu du rendu",
            "file": "Fichier (PDF, Word, ZIP, etc.)",
        }


class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["score", "feedback"]
        widgets = {
            "score": forms.NumberInput(attrs={"class": "form-control", "step": "0.5"}),
            "feedback": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }


class DisciplineForm(forms.ModelForm):
    class Meta:
        model = Discipline
        fields = [
            "name",
            "code",
            "description",
            "ects_credits",
            "semester",
            "is_active",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "code": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "ects_credits": forms.NumberInput(attrs={"class": "form-control"}),
            "semester": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            "name": "Nom de la matière",
            "code": "Code de la matière",
            "description": "Description",
            "ects_credits": "Crédits ECTS",
            "semester": "Semestre",
            "is_active": "Active",
        }
