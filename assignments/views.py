from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assignment, Submission, Discipline, Grade
from .forms import AssignmentForm, SubmissionForm, GradeForm, DisciplineForm

# === DEVOIRS ===
@login_required
def assignment_list(request):
    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        assignments = Assignment.objects.filter(teacher=request.user.teacher_profile)
    elif request.user.is_admin:
        assignments = Assignment.objects.all()
    else:
        assignments = Assignment.objects.filter(is_published=True)
    return render(request, 'assignments/list.html', {'assignments': assignments})

@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    submissions = None
    has_submission = False
    
    if request.user.is_student and hasattr(request.user, 'student_profile'):
        submissions = Submission.objects.filter(assignment=assignment, student=request.user.student_profile)
        has_submission = submissions.exists()
    elif request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        submissions = Submission.objects.filter(assignment=assignment)
    elif request.user.is_admin:
        submissions = Submission.objects.filter(assignment=assignment)
    
    return render(request, 'assignments/detail.html', {
        'assignment': assignment,
        'submissions': submissions,
        'has_submission': has_submission
    })

@login_required
def assignment_create(request):
    if not request.user.is_teacher and not request.user.is_admin:
        messages.error(request, 'Seuls les enseignants peuvent créer des devoirs')
        return redirect('home')

    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            if request.user.is_teacher:
                assignment.teacher = request.user.teacher_profile
            assignment.save()
            messages.success(request, 'Devoir créé avec succès !')
            return redirect('assignments:detail', pk=assignment.pk)
    else:
        form = AssignmentForm()
    return render(request, 'assignments/create.html', {'form': form})

@login_required
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.user.is_teacher and assignment.teacher != request.user.teacher_profile and not request.user.is_admin:
        messages.error(request, 'Vous n\'êtes pas autorisé à modifier ce devoir')
        return redirect('assignments:list')

    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Devoir modifié avec succès !')
            return redirect('assignments:detail', pk=assignment.pk)
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignments/edit.html', {'form': form, 'assignment': assignment})

@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.user.is_teacher and assignment.teacher != request.user.teacher_profile and not request.user.is_admin:
        messages.error(request, 'Vous n\'êtes pas autorisé à supprimer ce devoir')
        return redirect('assignments:list')

    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Devoir supprimé avec succès !')
        return redirect('assignments:list')
    return render(request, 'assignments/delete.html', {'assignment': assignment})

# === GESTION DES MATIÈRES (DISCIPLINES) ===
@login_required
def discipline_list(request):
    if not request.user.is_admin and not request.user.is_teacher:
        messages.error(request, 'Vous n\'avez pas accès à cette page')
        return redirect('home')
    
    disciplines = Discipline.objects.all()
    return render(request, 'assignments/disciplines/list.html', {'disciplines': disciplines})

@login_required
def discipline_create(request):
    if not request.user.is_admin and not request.user.is_teacher:
        messages.error(request, 'Vous n\'avez pas accès à cette page')
        return redirect('home')

    if request.method == 'POST':
        form = DisciplineForm(request.POST)
        if form.is_valid():
            discipline = form.save()
            messages.success(request, 'Matière créée avec succès !')
            return redirect('assignments:discipline_list')
    else:
        form = DisciplineForm()
    return render(request, 'assignments/disciplines/form.html', {'form': form, 'title': 'Ajouter une matière'})

@login_required
def discipline_edit(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    
    if not request.user.is_admin:
        messages.error(request, 'Seul un administrateur peut modifier une matière')
        return redirect('assignments:discipline_list')

    if request.method == 'POST':
        form = DisciplineForm(request.POST, instance=discipline)
        if form.is_valid():
            form.save()
            messages.success(request, 'Matière modifiée avec succès !')
            return redirect('assignments:discipline_list')
    else:
        form = DisciplineForm(instance=discipline)
    return render(request, 'assignments/disciplines/form.html', {'form': form, 'title': 'Modifier une matière'})

@login_required
def discipline_delete(request, pk):
    discipline = get_object_or_404(Discipline, pk=pk)
    
    if not request.user.is_admin:
        messages.error(request, 'Seul un administrateur peut supprimer une matière')
        return redirect('assignments:discipline_list')

    if request.method == 'POST':
        discipline.delete()
        messages.success(request, 'Matière supprimée avec succès !')
        return redirect('assignments:discipline_list')
    return render(request, 'assignments/disciplines/delete.html', {'discipline': discipline})
