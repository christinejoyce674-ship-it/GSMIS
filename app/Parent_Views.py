from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, F
from app.models import Learner, AcademicRecord, Parent, parent_notification, parent_feedback
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

def is_parent(user):
    return user.is_authenticated and user.groups.filter(name='Parent').exists()

@login_required
@user_passes_test(is_parent, login_url='/admin/login/')
def parent_home(request):
    return render(request, 'Parent/home.html', {})

@login_required
def parent_dashboard(request):
    parent = get_object_or_404(Parent, admin=request.user)
    
    # Get all children linked to this parent
    my_children = Learner.objects.filter(parent=parent).select_related('classe_id')
    
    # Get latest 5 notifications
    notifications = parent_notification.objects.filter(parent_id=parent).order_by('-created_at')[:5]

    context = {
        'parent': parent,
        'children': my_children,
        'notifications': notifications,
    }
    return render(request, 'Parents/home_learner.html', context)

# --- 2. ACADEMICS ---

@login_required

def view_report_card(request, learner_id):
    
    parent = get_object_or_404(Parent, admin=request.user)
    # Security: Ensure this child belongs to the logged-in parent
    learner = get_object_or_404(Learner, id=learner_id, parent=parent)
    
    records = AcademicRecord.objects.filter(learner=learner).select_related('subject')
    
    # Calculate total marks using F expressions to avoid None values
    total_score = 0
    for record in records:
        total_score += (record.mid or 0) + (record.eot or 0)

    context = {
        'learner': learner,
        'records': records,
        'total_score': total_score,
    }
    return render(request, 'Parents/report_card.html', context)

# --- 3. FEEDBACK ---

@login_required

def parent_feedback_save(request):
   
    parent = get_object_or_404(Parent, admin=request.user)
    
    if request.method == "POST":
        feedback_text = request.POST.get("feedback")
        if feedback_text:
            parent_feedback.objects.create(
                parent_id=parent,
                feedback=feedback_text,
                status=0
            )
            messages.success(request, "Your message has been sent to the office.")
            return redirect('parent_feedback')

    # Get history for this parent specifically
    feedback_history = parent_feedback.objects.filter(parent_id=parent).order_by('-created_at')
    
    return render(request, "Parents/feedback.html", {
        "feedback_history": feedback_history
    })

# --- 4. NOTIFICATIONS ---

@login_required

def parent_notifications_all(request):
    """
    View all historical notifications from the school.
    """
    parent = get_object_or_404(Parent, admin=request.user)
    notifications = parent_notification.objects.filter(parent_id=parent).order_by('-created_at')
    
    return render(request, "Parents/notification.html", {
        "notifications": notifications
    })