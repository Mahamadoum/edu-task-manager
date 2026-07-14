from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from assignments.models import Assignment, Submission, Grade
from assignments.forms import SubmissionForm, GradeForm

@login_required
def submission_create(request, assignment_pk):
    assignment = get_object_or_404(Assignment, pk=assignment_pk)
    
    if not request.user.is_student:
        messages.error(request, 'Seuls les étudiants peuvent rendre des devoirs')
        return redirect('assignments:detail', pk=assignment_pk)
    
    if not assignment.is_published:
        messages.error(request, 'Ce devoir n\'est pas encore publié')
        return redirect('assignments:detail', pk=assignment_pk)
    
    existing_submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user.student_profile
    ).first()
    
    if existing_submission:
        messages.warning(request, 'Vous avez déjà rendu ce devoir')
        return redirect('assignments:detail', pk=assignment_pk)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = request.user.student_profile
            submission.status = 'submitted'
            submission.save()
            messages.success(request, 'Devoir rendu avec succès !')
            return redirect('assignments:detail', pk=assignment_pk)
        else:
            messages.error(request, 'Erreur dans le formulaire')
    else:
        form = SubmissionForm()
    
    return render(request, 'submissions/create.html', {
        'form': form,
        'assignment': assignment
    })

@login_required
def grade_create(request, submission_pk):
    submission = get_object_or_404(Submission, pk=submission_pk)
    if not request.user.is_teacher:
        messages.error(request, 'Seuls les enseignants peuvent noter')
        return redirect('assignments:detail', pk=submission.assignment.pk)
    
    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.submission = submission
            grade.teacher = request.user.teacher_profile
            grade.save()
            submission.status = 'graded'
            submission.save()
            messages.success(request, 'Note attribuée avec succès !')
            return redirect('assignments:detail', pk=submission.assignment.pk)
    else:
        form = GradeForm()
    return render(request, 'submissions/grade.html', {
        'form': form,
        'submission': submission
    })
