import io, csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from app.models import (
    Learner, Teacher,  AcademicRecord,
    Subject,  staff_notification, staff_feedback
)

def is_teacher(user):
    return user.is_authenticated and user.groups.filter(name='Teachers').exists()

@login_required
@user_passes_test(is_teacher, login_url='/admin/login/')
def teacher_home(request):
    # Ensure we get the Teacher instance for the logged-in user
    teacher = get_object_or_404(Teacher, admin=request.user)

    subjects = Subject.objects.filter(staff=teacher)
    class_ids = subjects.values_list('classe_id', flat=True)
    total_students = Learner.objects.filter(classe_id__in=class_ids).count()

    context = {
        'teacher': teacher,
        'subjects': subjects,
        'total_students': total_students,
        'notifications_count': staff_notification.objects.filter(staff_id=teacher, status=0).count(),
    }
    return render(request, 'Staff/teacher_home.html', context)

@login_required
def upload_marks_csv(request):
    if request.method == "POST":
        file = request.FILES.get('file')
        if not file or not file.name.endswith('.csv'):
            messages.error(request, "Please upload a valid CSV file.")
            return redirect('upload_marks')

        try:
            data_set = file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.reader(io_string, delimiter=',', quotechar='"')
            next(reader)  # Skip Header

            for row in reader:
                # Expecting: row[0]=LearnerID, row[1]=SubjectName, row[2]=Term, row[3]=Mid, row[4]=EOT
                learner = Learner.objects.filter(learner_id=row[0]).first()
                subject = Subject.objects.filter(subject_name__iexact=row[1]).first()

                if learner and subject:
                    AcademicRecord.objects.update_or_create(
                        learner=learner,
                        subject=subject,
                        term=int(row[2]),
                        defaults={
                            'mid': float(row[3]) if row[3] else 0,
                            'eot': float(row[4]) if row[4] else 0,
                        }
                    )

            messages.success(request, 'Marks processed successfully!')
        except Exception as e:
            messages.error(request, f"Error processing file: {e}")

        return redirect('teacher_home')

    return render(request, 'Staff/upload_marks.html')

# --- 3. FEEDBACK & NOTIFICATIONS ---

@login_required
def staff_feedback_save(request):
    teacher = get_object_or_404(Teacher, admin=request.user)

    if request.method == "POST":
        feedback_text = request.POST.get("feedback")
        staff_feedback.objects.create(
            staff_id=teacher,
            feedback=feedback_text,
            status=0
        )
        messages.success(request, "Feedback submitted successfully!")
        return redirect('staff_feedback')

    feedback_history = staff_feedback.objects.filter(staff_id=teacher).order_by('-created_at')
    return render(request, "Staff/feedback.html", {"feedback_history": feedback_history})

@login_required
def staff_notifications_all(request):
    teacher = get_object_or_404(Teacher, admin=request.user)
    notifications = staff_notification.objects.filter(staff_id=teacher).order_by('-created_at')
    return render(request, "Staff/notification.html", {"notification": notifications})