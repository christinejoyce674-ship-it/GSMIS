import io
import csv
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from app.models import (
    Learner, Teacher, AcademicRecord,
    Subject, staff_notification, staff_feedback
)


def is_teacher(user):
    return str(getattr(user, 'user_type', '')) == '2'


@login_required(login_url='app:login')
@user_passes_test(is_teacher, login_url='app:login')
def teacher_home(request):
    teacher = get_object_or_404(Teacher, admin=request.user)
    subjects = Subject.objects.filter(staff=teacher).select_related('classe_id')
    class_ids = subjects.values_list('classe_id', flat=True)
    total_learners = Learner.objects.filter(classe_id__in=class_ids).count()

    context = {
        'teacher': teacher,
        'subjects': subjects,
        'total_learners': total_learners,
        'notifications_count': staff_notification.objects.filter(staff_id=teacher, status=0).count(),
    }
    return render(request, 'staff/teacher_home.html', context)


@login_required(login_url='app:login')
@user_passes_test(is_teacher, login_url='app:login')
def upload_marks_csv(request, classe_id=None):
    teacher = get_object_or_404(Teacher, admin=request.user)
    subjects = Subject.objects.filter(staff=teacher).select_related('classe_id')
    
    if request.method == "POST":
        file = request.FILES.get('file')
        if not file:
            messages.error(request, "Please select a CSV file to upload.")
            return redirect('app:upload_marks', classe_id=classe_id)
        
        if not file.name.endswith('.csv'):
            messages.error(request, "Invalid file format. Please upload a .csv file.")
            return redirect('app:upload_marks', classe_id=classe_id)

        try:
            data_set = file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            reader = csv.reader(io_string, delimiter=',', quotechar='"')
            header = next(reader, None)  # skip header row
            
            if header is None:
                messages.error(request, "The CSV file is empty.")
                return redirect('app:upload_marks', classe_id=classe_id)

            processed = 0
            skipped = 0
            errors = []
            
            for line_num, row in enumerate(reader, start=2):
                if len(row) < 5:
                    skipped += 1
                    errors.append(f"Line {line_num}: Insufficient columns (expected at least 5).")
                    continue

                # Expected format: [learner_id, subject_name, term, mid, eot]
                l_id = row[0].strip()
                s_name = row[1].strip()
                
                learner = Learner.objects.filter(learner_id=l_id).first()
                # Find the subject belonging to this teacher by name
                subject = subjects.filter(subject_name__iexact=s_name).first()

                if learner and subject:
                    try:
                        term = int(row[2])
                        mid = float(row[3]) if row[3].strip() else 0
                        eot = float(row[4]) if row[4].strip() else 0
                        
                        AcademicRecord.objects.update_or_create(
                            learner=learner,
                            subject=subject,
                            term=term,
                            defaults={'mid': mid, 'eot': eot},
                        )
                        processed += 1
                    except (ValueError, TypeError) as e:
                        skipped += 1
                        errors.append(f"Line {line_num}: Data format error ({str(e)}).")
                else:
                    skipped += 1
                    if not learner:
                        errors.append(f"Line {line_num}: Learner ID '{l_id}' not found.")
                    if not subject:
                        errors.append(f"Line {line_num}: Subject '{s_name}' not assigned to you.")

            if processed > 0:
                messages.success(request, f'Successfully processed {processed} records.')
            if skipped > 0:
                messages.warning(request, f'Skipped {skipped} records due to errors.')
                for err in errors[:5]: # Show first 5 errors
                    messages.info(request, err)
                if len(errors) > 5:
                    messages.info(request, f"...and {len(errors)-5} more errors.")
                    
        except Exception as e:
            messages.error(request, f"Fatal Processing Error: {str(e)}")

        return redirect('app:teacher_home')

    context = {
        'subjects': subjects,
        'classe_id': classe_id,
        'notifications_count': staff_notification.objects.filter(staff_id=teacher, status=0).count(),
    }
    return render(request, 'staff/upload_marks.html', context)


@login_required(login_url='app:login')
@user_passes_test(is_teacher, login_url='app:login')
def staff_feedback_save(request):
    teacher = get_object_or_404(Teacher, admin=request.user)

    if request.method == "POST":
        feedback_text = request.POST.get("feedback", "").strip()
        if not feedback_text:
            messages.error(request, "Feedback cannot be empty.")
            return redirect('app:staff_feedback')
        staff_feedback.objects.create(
            staff_id=teacher,
            feedback=feedback_text,
            status=0
        )
        messages.success(request, "Feedback submitted successfully!")
        return redirect('app:staff_feedback')

    feedback_history = staff_feedback.objects.filter(staff_id=teacher).order_by('-created_at')
    return render(request, "staff/staff_feedback.html", {"feedback_history": feedback_history})


@login_required(login_url='app:login')
@user_passes_test(is_teacher, login_url='app:login')
def staff_notifications_all(request):
    teacher = get_object_or_404(Teacher, admin=request.user)
    notifications = staff_notification.objects.filter(staff_id=teacher).order_by('-created_at')
    return render(request, "staff/staff_notifications.html", {"notifications": notifications})