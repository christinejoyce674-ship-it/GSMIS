from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponseForbidden
from django.contrib import messages
from app.models import Learner, AcademicRecord, Parent, parent_notification, parent_feedback


def is_parent(user):
    return str(getattr(user, 'user_type', '')) == '3'


@login_required(login_url='app:login')
@user_passes_test(is_parent, login_url='app:login')
def parent_dashboard(request):
    parent = get_object_or_404(Parent, admin=request.user)
    my_children = Learner.objects.filter(parent=parent).select_related('classe_id')
    notifications = parent_notification.objects.filter(parent_id=parent).order_by('-created_at')[:5]

    context = {
        'parent': parent,
        'children': my_children,
        'notifications': notifications,
    }
    return render(request, 'parent/parent_dashboard.html', context)


@login_required(login_url='app:login')
@user_passes_test(is_parent, login_url='app:login')
def view_report_card(request, learner_id):
    parent = get_object_or_404(Parent, admin=request.user)

    # Security: Ensure this child belongs to the logged-in parent
    learner = get_object_or_404(Learner, id=learner_id, parent=parent)

    # Block access if fees not paid
    if not learner.fees_paid:
        return render(request, 'parent/fees_blocked.html', {'learner': learner})

    # Get selected term from query parameter, default to latest term
    selected_term = request.GET.get('term', None)
    
    # Get all records for this learner with proper relationships
    records = AcademicRecord.objects.filter(
        learner=learner
    ).select_related('subject').order_by('subject__subject_name')
    
    # Filter by term if specified
    if selected_term:
        records = records.filter(term=int(selected_term))
    
    # Get available terms for this learner
    available_terms = AcademicRecord.objects.filter(
        learner=learner
    ).values_list('term', flat=True).distinct().order_by('term')
    
    # Get term summary if exists
    from app.models import TermSummary
    term_summary = None
    if selected_term:
        term_summary = TermSummary.objects.filter(
            learner=learner, 
            term=int(selected_term)
        ).first()
    
    # Calculate statistics
    total_marks = 0
    total_subjects = 0
    grade_counts = {}
    
    for record in records:
        total_marks += record.final_weighted_mark
        total_subjects += 1
        
        # Count grades
        grade = record.score or 'N/A'
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    
    # Calculate average
    average_mark = round(total_marks / total_subjects, 2) if total_subjects > 0 else 0
    
    # Calculate position in class
    position = None
    total_learners = 0
    
    if selected_term and total_subjects > 0:
        # Get all learners in the same class
        class_learners = Learner.objects.filter(classe_id=learner.classe_id)
        total_learners = class_learners.count()
        
        # Calculate average for each learner in the class
        learner_averages = []
        for class_learner in class_learners:
            learner_records = AcademicRecord.objects.filter(
                learner=class_learner,
                term=int(selected_term)
            )
            
            if learner_records.exists():
                learner_total = sum(r.final_weighted_mark for r in learner_records)
                learner_count = learner_records.count()
                learner_avg = learner_total / learner_count if learner_count > 0 else 0
                learner_averages.append({
                    'learner_id': class_learner.id,
                    'average': learner_avg
                })
        
        # Sort by average (descending) and find position
        learner_averages.sort(key=lambda x: x['average'], reverse=True)
        
        for idx, item in enumerate(learner_averages, start=1):
            if item['learner_id'] == learner.id:
                position = idx
                break

    context = {
        'learner': learner,
        'records': records,
        'total_marks': total_marks,
        'average_mark': average_mark,
        'total_subjects': total_subjects,
        'grade_counts': grade_counts,
        'available_terms': available_terms,
        'selected_term': int(selected_term) if selected_term else None,
        'term_summary': term_summary,
        'position': position,
        'total_learners': total_learners,
    }
    return render(request, 'parent/view_report_card.html', context)


@login_required(login_url='app:login')
@user_passes_test(is_parent, login_url='app:login')
def parent_feedback_view(request):
    parent = get_object_or_404(Parent, admin=request.user)

    if request.method == "POST":
        feedback_text = request.POST.get("feedback", "").strip()
        if feedback_text:
            parent_feedback.objects.create(
                parent_id=parent,
                feedback=feedback_text,
                status=0
            )
            messages.success(request, "Your message has been sent to the office.")
            return redirect('app:parent_feedback')

    feedback_history = parent_feedback.objects.filter(parent_id=parent).order_by('-created_at')
    return render(request, "parent/feedback.html", {"feedback_history": feedback_history})


@login_required(login_url='app:login')
@user_passes_test(is_parent, login_url='app:login')
def parent_notifications_all(request):
    parent = get_object_or_404(Parent, admin=request.user)
    notifications = parent_notification.objects.filter(parent_id=parent).order_by('-created_at')
    return render(request, "parent/notification.html", {"notifications": notifications})


@login_required(login_url='app:login')
@user_passes_test(is_parent, login_url='app:login')
def view_midterm_report(request, learner_id):
    """Mid-term report showing only mid-term marks"""
    parent = get_object_or_404(Parent, admin=request.user)

    # Security: Ensure this child belongs to the logged-in parent
    learner = get_object_or_404(Learner, id=learner_id, parent=parent)

    # Block access if fees not paid
    if not learner.fees_paid:
        return render(request, 'parent/fees_blocked.html', {'learner': learner})

    # Get selected term from query parameter
    selected_term = request.GET.get('term', None)

    # Get all records for this learner
    records = AcademicRecord.objects.filter(
        learner=learner
    ).select_related('subject').order_by('subject__subject_name')

    # Filter by term if specified
    if selected_term:
        records = records.filter(term=int(selected_term))

    # Get available terms
    available_terms = AcademicRecord.objects.filter(
        learner=learner
    ).values_list('term', flat=True).distinct().order_by('term')

    # Calculate statistics based on mid-term marks only
    total_mid_marks = 0
    total_subjects = 0

    for record in records:
        total_mid_marks += record.mid
        total_subjects += 1

    # Calculate average
    average_mid_mark = round(total_mid_marks / total_subjects, 2) if total_subjects > 0 else 0

    # Calculate position based on mid-term average
    position = None
    total_learners = 0

    if selected_term and total_subjects > 0:
        class_learners = Learner.objects.filter(classe_id=learner.classe_id)
        total_learners = class_learners.count()

        # Calculate mid-term average for each learner
        learner_averages = []
        for class_learner in class_learners:
            learner_records = AcademicRecord.objects.filter(
                learner=class_learner,
                term=int(selected_term)
            )

            if learner_records.exists():
                learner_mid_total = sum(r.mid for r in learner_records)
                learner_count = learner_records.count()
                learner_avg = learner_mid_total / learner_count if learner_count > 0 else 0
                learner_averages.append({
                    'learner_id': class_learner.id,
                    'average': learner_avg
                })

        # Sort by average (descending) and find position
        learner_averages.sort(key=lambda x: x['average'], reverse=True)

        for idx, item in enumerate(learner_averages, start=1):
            if item['learner_id'] == learner.id:
                position = idx
                break

    context = {
        'learner': learner,
        'records': records,
        'total_mid_marks': total_mid_marks,
        'average_mid_mark': average_mid_mark,
        'total_subjects': total_subjects,
        'available_terms': available_terms,
        'selected_term': int(selected_term) if selected_term else None,
        'position': position,
        'total_learners': total_learners,
    }
    return render(request, 'parent/view_midterm_report.html', context)

