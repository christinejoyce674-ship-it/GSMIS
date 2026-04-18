import uuid
from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Avg
from app.models import (
    Classe, Learner, AcademicRecord, TermSummary, Teacher, Subject,
    SessionYear, Parent, CustomUser, Event,
    parent_notification as ParentNotification, 
    staff_notification as StaffNotification, 
    parent_feedback as ParentFeedback, 
    staff_feedback as StaffFeedback
)

def is_hod(user):
    return str(getattr(user, 'user_type', '')) in ['1', '4'] and user.is_authenticated

# ── HOD DASHBOARD ─────────────────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_home(request):
    classes = Classe.objects.all()
    total_learners = Learner.objects.count()
    total_staff = Teacher.objects.count()
    total_parents = Parent.objects.count()
    fees_unpaid = Learner.objects.filter(fees_paid=False).count()

    class_averages = (
        AcademicRecord.objects
        .values('learner__classe_id__class_name')
        .annotate(avg_score=Avg('final_weighted_mark'))
    )
    pass_count = AcademicRecord.objects.filter(eot__gte=50).count()
    fail_count = AcademicRecord.objects.filter(eot__lt=50).count()

    class_labels = [item['learner__classe_id__class_name'] for item in class_averages]
    class_scores = [round(item['avg_score'], 1) if item['avg_score'] else 0 for item in class_averages]

    context = {
        'classes': classes,
        'total_learners': total_learners,
        'total_staff': total_staff,
        'total_parents': total_parents,
        'fees_unpaid': fees_unpaid,
        'class_averages': class_averages,
        'class_labels': class_labels,
        'class_scores': class_scores,
        'pass_count': pass_count,
        'fail_count': fail_count,
    }
    return render(request, 'HOD/hod_home.html', context)

# ── LEARNER MANAGEMENT ────────────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_add_learner(request):
    sessions = SessionYear.objects.all()
    classes = Classe.objects.all()
    parents = Parent.objects.select_related("admin").all()

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        learner_id = request.POST.get("learner_id", "").strip()
        gender = request.POST.get("gender", "")
        religion = request.POST.get("religion", "")
        section = request.POST.get("section", "D")
        nationality = request.POST.get("nationality", "Ugandan").strip()
        health_issue = request.POST.get("health_issue", "").strip()
        parent_mobile = request.POST.get("parent_mobile_number", "").strip()
        relationship = request.POST.get("relationship_with_learner", "").strip()
        dob_str = request.POST.get("date_of_birth", "")
        classe_id_val = request.POST.get("classe_id")
        session_id_val = request.POST.get("session_year_id")
        parent_id_val = request.POST.get("parent_id")

        if not all([first_name, last_name, learner_id, gender, religion, classe_id_val]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, "HOD/add_learner.html", {
                "sessions": sessions, "classe": classes, "parents": parents
            })

        if Learner.objects.filter(learner_id=learner_id).exists():
            messages.error(request, f"A learner with ID '{learner_id}' already exists.")
            return render(request, "HOD/add_learner.html", {
                "sessions": sessions, "classe": classes, "parents": parents
            })

        dob = None
        if dob_str:
            try:
                dob = date.fromisoformat(dob_str)
            except ValueError:
                messages.error(request, "Invalid date of birth format. Use YYYY-MM-DD.")
                return render(request, "HOD/add_learner.html", {
                    "sessions": sessions, "classe": classes, "parents": parents
                })

        username = learner_id
        email = f"{learner_id}@school.local"
        password = uuid.uuid4().hex[:12]
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type="5",
        )

        classe_obj = get_object_or_404(Classe, id=classe_id_val)
        session_obj = get_object_or_404(SessionYear, id=session_id_val) if session_id_val else None
        parent_obj = get_object_or_404(Parent, id=parent_id_val) if parent_id_val else None

        Learner.objects.create(
            admin=user,
            first_name=first_name,
            last_name=last_name,
            learner_id=learner_id,
            gender=gender,
            religion=religion,
            section=section,
            nationality=nationality,
            health_issue=health_issue or None,
            parent_mobile_number=parent_mobile or None,
            relationship_with_learner=relationship or None,
            date_of_birth=dob,
            classe_id=classe_obj,
            session_year_id=session_obj,
            parent=parent_obj,
        )

        messages.success(request, f"Learner '{first_name} {last_name}' added successfully!")
        return redirect("app:view_learners")

    return render(request, "HOD/add_learner.html", {
        "sessions": sessions,
        "classe": classes,
        "parents": parents,
    })

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_view_learners(request):
    learners = Learner.objects.select_related(
        "admin", "parent__admin", "classe_id", "session_year_id"
    ).all()
    return render(request, "HOD/view_learners.html", {"learners": learners})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_update_learner(request, learner_id):
    learner = get_object_or_404(Learner, id=learner_id)

    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        if first_name:
            learner.admin.first_name = first_name
            learner.first_name = first_name
        if last_name:
            learner.admin.last_name = last_name
            learner.last_name = last_name

        if request.FILES.get("profile_pic"):
            learner.admin.profile_pic = request.FILES["profile_pic"]

        learner.admin.save()

        learner.learner_id = request.POST.get("learner_id", learner.learner_id)
        learner.gender = request.POST.get("gender", learner.gender)
        learner.religion = request.POST.get("religion", learner.religion)

        dob = request.POST.get("date_of_birth")
        if dob:
            try:
                learner.date_of_birth = date.fromisoformat(dob)
            except ValueError:
                messages.error(request, "Invalid date of birth format. Use YYYY-MM-DD.")
                return redirect("app:update_learner", learner_id=learner.id)

        classe_id = request.POST.get("classe_id")
        if classe_id:
            learner.classe_id = get_object_or_404(Classe, id=classe_id)

        learner.section = request.POST.get("section", learner.section)

        session_id = request.POST.get("session_year_id")
        if session_id:
            learner.session_year_id = get_object_or_404(SessionYear, id=session_id)

        learner.nationality = request.POST.get("nationality", learner.nationality)
        learner.health_issue = request.POST.get("health_issue", learner.health_issue)

        parent_id = request.POST.get("parent_id")
        if parent_id:
            learner.parent = get_object_or_404(Parent, id=parent_id)

        learner.parent_mobile_number = request.POST.get(
            "parent_mobile_number", learner.parent_mobile_number
        )

        learner.save()
        messages.success(request, "Learner updated successfully.")
        return redirect("app:view_learners")

    context = {
        "learner": learner,
        "classe": Classe.objects.all(),
        "session_year": SessionYear.objects.all(),
        "parents": Parent.objects.all(),
    }
    return render(request, "HOD/update_learner.html", context)

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_delete_learner(request, learner_id):
    learner = get_object_or_404(Learner, id=learner_id)
    user = learner.admin
    user.delete()
    messages.success(request, "Learner deleted successfully.")
    return redirect("app:view_learners")

# ── STAFF MANAGEMENT ──────────────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_add_staff(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        teacher_id = request.POST.get("teacher_id", "").strip()
        gender = request.POST.get("gender", "")
        qualification = request.POST.get("qualification", "").strip()
        address = request.POST.get("address", "").strip()

        if not all([first_name, last_name, email, username, password, teacher_id]):
            messages.error(request, "Please fill in all required fields.")
            return render(request, "HOD/add_staff.html")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, f"Username '{username}' is already taken.")
            return render(request, "HOD/add_staff.html")

        if Teacher.objects.filter(teacher_id=teacher_id).exists():
            messages.error(request, f"Teacher ID '{teacher_id}' already exists.")
            return render(request, "HOD/add_staff.html")

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type="2",
        )
        if request.FILES.get("profile_pic"):
            user.profile_pic = request.FILES["profile_pic"]
            user.save()

        Teacher.objects.create(
            admin=user,
            teacher_id=teacher_id,
            teacher_name=f"{first_name} {last_name}",
            gender=gender,
            qualification=qualification,
            address=address,
        )
        messages.success(request, f"Teacher '{first_name} {last_name}' added successfully!")
        return redirect("app:view_staff")

    return render(request, "HOD/add_staff.html")

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_view_staff(request):
    staff_members = Teacher.objects.select_related('admin').all()
    return render(request, 'HOD/view_staff.html', {'staff': staff_members})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_update_staff(request, staff_id):
    staff = get_object_or_404(Teacher, id=staff_id)
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password", "").strip()

        if first_name:
            staff.admin.first_name = first_name
        if last_name:
            staff.admin.last_name = last_name
        if username:
            staff.admin.username = username
        if email:
            staff.admin.email = email
        if request.FILES.get("profile_pic"):
            staff.admin.profile_pic = request.FILES["profile_pic"]
        if password:
            staff.admin.set_password(password)
        staff.admin.save()

        staff.teacher_id = request.POST.get("teacher_id", staff.teacher_id)
        staff.gender = request.POST.get("gender", staff.gender)
        staff.qualification = request.POST.get("qualification", staff.qualification)
        staff.address = request.POST.get("address", staff.address)
        staff.teacher_name = f"{staff.admin.first_name} {staff.admin.last_name}"

        staff.save()
        messages.success(request, "Teacher updated.")
        return redirect("app:view_staff")

    return render(request, "HOD/update_staff.html", {"staff": staff})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_delete_staff(request, staff_id):
    staff = get_object_or_404(Teacher, id=staff_id)
    user = staff.admin
    user.delete()
    messages.success(request, "Staff member deleted.")
    return redirect("app:view_staff")

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_promote_staff(request, staff_id):
    staff = get_object_or_404(Teacher, id=staff_id)
    user = staff.admin
    user.user_type = "4"
    user.save()
    messages.success(request, f"{user.first_name} {user.last_name} promoted to HOD.")
    return redirect("app:view_staff")

# ── PARENT MANAGEMENT ─────────────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_add_parent(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        address = request.POST.get("address", "").strip()

        if not all([first_name, last_name, username, email, password]):
            messages.error(request, "All fields are required.")
            return render(request, "HOD/add_parent.html")

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, "HOD/add_parent.html")

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type="3"
        )
        Parent.objects.create(admin=user, address=address)
        messages.success(request, "Parent added successfully!")
        return redirect("app:view_parent")
    return render(request, "HOD/add_parent.html")

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_view_parent(request):
    parents = Parent.objects.select_related("admin").all()
    return render(request, "HOD/view_parent.html", {"parents": parents})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_update_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    if request.method == "POST":
        parent.admin.first_name = request.POST.get("first_name", parent.admin.first_name)
        parent.admin.last_name = request.POST.get("last_name", parent.admin.last_name)
        parent.admin.email = request.POST.get("email", parent.admin.email)
        parent.address = request.POST.get("address", parent.address)
        
        password = request.POST.get("password")
        if password:
            parent.admin.set_password(password)
            
        parent.admin.save()
        parent.save()
        messages.success(request, "Parent updated successfully!")
        return redirect("app:view_parent")
    return render(request, "HOD/update_parent.html", {"parent": parent})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_delete_parent(request, parent_id):
    parent = get_object_or_404(Parent, id=parent_id)
    user = parent.admin
    user.delete()
    messages.success(request, "Parent deleted.")
    return redirect("app:view_parent")

# ── CLASS MANAGEMENT ──────────────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_add_class(request):
    if request.method == "POST":
        class_name = request.POST.get("class_name")
        if class_name:
            Classe.objects.create(class_name=class_name)
            messages.success(request, "Class added.")
            return redirect("app:view_class")
    return render(request, "HOD/add_class.html")

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_view_class(request):
    classes = Classe.objects.all()
    return render(request, "HOD/view_class.html", {"classes": classes})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_update_class(request, class_id):
    classe = get_object_or_404(Classe, id=class_id)
    if request.method == "POST":
        class_name = request.POST.get("class_name")
        if class_name:
            classe.class_name = class_name
            classe.save()
            messages.success(request, "Class updated.")
            return redirect("app:view_class")
    return render(request, "HOD/update_class.html", {"classe": classe})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_delete_class(request, class_id):
    classe = get_object_or_404(Classe, id=class_id)
    classe.delete()
    messages.success(request, "Class deleted.")
    return redirect("app:view_class")

# ── SUBJECT MANAGEMENT ────────────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_add_subject(request):
    classes = Classe.objects.all()
    staff = Teacher.objects.select_related("admin").all()
    if request.method == "POST":
        subject_name = request.POST.get("subject_name", "").strip()
        classe_id = request.POST.get("classe_id")
        staff_id = request.POST.get("staff_id")
        if not subject_name or not classe_id:
            messages.error(request, "Subject name and class are required.")
            return render(request, "HOD/add_subject.html", {"classe": classes, "staff": staff})
        classe_obj = get_object_or_404(Classe, id=classe_id)
        staff_obj = get_object_or_404(Teacher, id=staff_id) if staff_id else None
        Subject.objects.create(subject_name=subject_name, classe_id=classe_obj, staff=staff_obj)
        messages.success(request, "Subject added successfully!")
        return redirect("app:view_subject")
    return render(request, "HOD/add_subject.html", {"classe": classes, "staff": staff})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_view_subject(request):
    subjects = Subject.objects.select_related("classe_id", "staff__admin").all()
    return render(request, "HOD/view_subject.html", {"subjects": subjects})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_update_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == "POST":
        subject.subject_name = request.POST.get("subject_name", subject.subject_name)
        classe_id = request.POST.get("classe_id")
        if classe_id:
            subject.classe_id = get_object_or_404(Classe, id=classe_id)
        staff_id = request.POST.get("staff_id")
        subject.staff = get_object_or_404(Teacher, id=staff_id) if staff_id else None
        subject.save()
        messages.success(request, "Subject updated.")
        return redirect("app:view_subject")
    context = {
        "subject": subject,
        "classe": Classe.objects.all(),
        "staff": Teacher.objects.select_related("admin").all(),
    }
    return render(request, "HOD/update_subject.html", context)

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    subject.delete()
    messages.success(request, "Subject deleted.")
    return redirect("app:view_subject")

# ── SESSION MANAGEMENT ────────────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_add_session(request):
    if request.method == "POST":
        start = request.POST.get("session_year_start")
        end = request.POST.get("session_year_end")
        if start and end:
            SessionYear.objects.create(session_start=start, session_end=end)
            messages.success(request, "Session created.")
            return redirect("app:view_session")
    return render(request, "HOD/add_session.html")

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_view_session(request):
    sessions = SessionYear.objects.all()
    return render(request, "HOD/view_session.html", {"session": sessions})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_update_session(request, session_id):
    session = get_object_or_404(SessionYear, id=session_id)
    if request.method == "POST":
        start = request.POST.get("session_year_start")
        end = request.POST.get("session_year_end")
        if start and end:
            session.session_start = start
            session.session_end = end
            session.save()
            messages.success(request, "Session updated.")
            return redirect("app:view_session")
    return render(request, "HOD/update_session.html", {"session": session})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_delete_session(request, session_id):
    session = get_object_or_404(SessionYear, id=session_id)
    session.delete()
    messages.success(request, "Session deleted.")
    return redirect("app:view_session")

# ── REPORTS & BROADSHEET ──────────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_broadsheet(request, class_id):
    target_class = get_object_or_404(Classe, id=class_id)
    learners = Learner.objects.filter(classe_id=target_class).prefetch_related(
        'academicrecord_set__subject'
    ).select_related('admin')
    subjects = Subject.objects.filter(classe_id=target_class)

    context = {
        'target_class': target_class,
        'learners': learners,
        'subjects': subjects,
    }
    return render(request, 'HOD/hod_broadsheet.html', context)

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_class_statistics(request, class_id):
    """View class performance statistics with mean, median, and standard deviation"""
    target_class = get_object_or_404(Classe, id=class_id)

    # Get selected term from query parameter
    selected_term = request.GET.get('term', None)

    if not selected_term:
        messages.warning(request, "Please select a term to view statistics.")
        return redirect('app:hod_broadsheet', class_id=class_id)

    # Get all learners in this class
    learners = Learner.objects.filter(classe_id=target_class)

    # Get all subjects for this class
    subjects = Subject.objects.filter(classe_id=target_class)

    # Calculate statistics for each subject
    subject_statistics = []

    for subject in subjects:
        # Get all records for this subject and term
        records = AcademicRecord.objects.filter(
            subject=subject,
            term=int(selected_term),
            learner__classe_id=target_class
        )

        if records.exists():
            # Extract MID and EOT scores
            mid_scores = [r.mid for r in records]
            eot_scores = [r.eot for r in records]
            final_scores = [r.final_weighted_mark for r in records]

            # Calculate statistics for MID
            mid_mean = sum(mid_scores) / len(mid_scores)
            mid_sorted = sorted(mid_scores)
            mid_median = mid_sorted[len(mid_sorted) // 2] if len(mid_sorted) % 2 == 1 else (mid_sorted[len(mid_sorted) // 2 - 1] + mid_sorted[len(mid_sorted) // 2]) / 2
            mid_variance = sum((x - mid_mean) ** 2 for x in mid_scores) / len(mid_scores)
            mid_std_dev = mid_variance ** 0.5

            # Calculate statistics for EOT
            eot_mean = sum(eot_scores) / len(eot_scores)
            eot_sorted = sorted(eot_scores)
            eot_median = eot_sorted[len(eot_sorted) // 2] if len(eot_sorted) % 2 == 1 else (eot_sorted[len(eot_sorted) // 2 - 1] + eot_sorted[len(eot_sorted) // 2]) / 2
            eot_variance = sum((x - eot_mean) ** 2 for x in eot_scores) / len(eot_scores)
            eot_std_dev = eot_variance ** 0.5

            # Calculate statistics for Final
            final_mean = sum(final_scores) / len(final_scores)
            final_sorted = sorted(final_scores)
            final_median = final_sorted[len(final_sorted) // 2] if len(final_sorted) % 2 == 1 else (final_sorted[len(final_sorted) // 2 - 1] + final_sorted[len(final_sorted) // 2]) / 2
            final_variance = sum((x - final_mean) ** 2 for x in final_scores) / len(final_scores)
            final_std_dev = final_variance ** 0.5

            subject_statistics.append({
                'subject': subject,
                'count': len(records),
                'mid_mean': round(mid_mean, 2),
                'mid_median': round(mid_median, 2),
                'mid_std_dev': round(mid_std_dev, 2),
                'eot_mean': round(eot_mean, 2),
                'eot_median': round(eot_median, 2),
                'eot_std_dev': round(eot_std_dev, 2),
                'final_mean': round(final_mean, 2),
                'final_median': round(final_median, 2),
                'final_std_dev': round(final_std_dev, 2),
            })

    # Get available terms
    available_terms = AcademicRecord.objects.filter(
        learner__classe_id=target_class
    ).values_list('term', flat=True).distinct().order_by('term')

    context = {
        'target_class': target_class,
        'subject_statistics': subject_statistics,
        'selected_term': int(selected_term),
        'available_terms': available_terms,
        'total_learners': learners.count(),
    }
    return render(request, 'HOD/class_statistics.html', context)


@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_view_learner_report(request, learner_id):
    learner = get_object_or_404(Learner, id=learner_id)
    records = AcademicRecord.objects.filter(learner=learner).select_related('subject').order_by('term', 'subject__subject_name')
    summaries = TermSummary.objects.filter(learner=learner).order_by('term')
    
    # Calculate statistics per term including position
    term_stats = {}
    for record in records:
        if record.term not in term_stats:
            term_stats[record.term] = {
                'total': 0,
                'count': 0,
                'grades': {},
                'position': None,
                'total_learners': 0
            }
        term_stats[record.term]['total'] += record.final_weighted_mark
        term_stats[record.term]['count'] += 1
        grade = record.score or 'N/A'
        term_stats[record.term]['grades'][grade] = term_stats[record.term]['grades'].get(grade, 0) + 1
    
    # Calculate averages and positions for each term
    for term in term_stats:
        if term_stats[term]['count'] > 0:
            term_stats[term]['average'] = round(term_stats[term]['total'] / term_stats[term]['count'], 2)
            
            # Calculate position for this term
            class_learners = Learner.objects.filter(classe_id=learner.classe_id)
            term_stats[term]['total_learners'] = class_learners.count()
            
            # Calculate average for each learner in the class for this term
            learner_averages = []
            for class_learner in class_learners:
                learner_records = AcademicRecord.objects.filter(
                    learner=class_learner,
                    term=term
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
                    term_stats[term]['position'] = idx
                    break

    context = {
        'learner': learner,
        'records': records,
        'summaries': summaries,
        'term_stats': term_stats,
    }
    return render(request, 'HOD/hod_report.html', context)

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_update_term_summary(request, learner_id, term):
    learner = get_object_or_404(Learner, id=learner_id)
    summary, created = TermSummary.objects.get_or_create(
        learner=learner, term=term, defaults={'days_present': 0, 'days_absent': 0}
    )
    if request.method == 'POST':
        summary.days_present = request.POST.get('days_present', summary.days_present)
        summary.days_absent = request.POST.get('days_absent', summary.days_absent)
        summary.teacher_comment = request.POST.get('teacher_comment', summary.teacher_comment)
        summary.headteacher_remark = request.POST.get('headteacher_remark', summary.headteacher_remark)
        summary.save()
        messages.success(request, f"Term {term} summary updated for {learner}.")
        return redirect('app:hod_learner_report', learner_id=learner_id)
    context = {"learner": learner, "summary": summary, "term": term}
    return render(request, 'HOD/hod_term_summary_form.html', context)

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_toggle_fees(request, learner_id):
    learner = get_object_or_404(Learner, id=learner_id)
    if request.method == 'POST':
        value = request.POST.get('fees_paid', '')
        learner.fees_paid = (value == 'yes')
        learner.save()
        messages.success(request, f"Fees status updated for {learner.first_name}.")
        return redirect('app:hod_learner_report', learner_id=learner_id)
    return redirect('app:hod_home')

# ── NOTIFICATIONS & FEEDBACK ──────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_send_staff_notification(request):
    staff_members = Teacher.objects.select_related("admin").all()
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        message_text = request.POST.get("message")
        staff_obj = get_object_or_404(Teacher, id=staff_id)
        StaffNotification.objects.create(staff_id=staff_obj, message=message_text)
        messages.success(request, "Notification sent to staff!")
        return redirect("app:add_staff_notification")
    return render(request, "HOD/staff_notification.html", {"staff": staff_members})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_send_parent_notification(request):
    parents = Parent.objects.select_related("admin").all()
    if request.method == "POST":
        parent_id = request.POST.get("parent_id")
        message_text = request.POST.get("message")
        parent_obj = get_object_or_404(Parent, id=parent_id)
        ParentNotification.objects.create(parent_id=parent_obj, message=message_text)
        messages.success(request, "Notification sent to parent!")
        return redirect("app:add_parent_notification")
    return render(request, "HOD/parent_notification.html", {"parents": parents})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_staff_feedback_view(request):
    feedback = StaffFeedback.objects.all().order_by("-created_at")
    return render(request, "HOD/staff_feedback_list.html", {"feedback": feedback})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_parent_feedback_view(request):
    feedback = ParentFeedback.objects.all().order_by("-created_at")
    return render(request, "HOD/parent_feedback_list.html", {"feedback": feedback})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_staff_feedback_reply(request):
    if request.method == "POST":
        f_id = request.POST.get("feedback_id")
        reply_txt = request.POST.get("reply")
        fobj = get_object_or_404(StaffFeedback, id=f_id)
        fobj.reply = reply_txt
        fobj.status = 1
        fobj.save()
        messages.success(request, "Reply sent.")
    return redirect("app:staff_feedback_view")

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_parent_feedback_reply(request):
    if request.method == "POST":
        f_id = request.POST.get("feedback_id")
        reply_txt = request.POST.get("reply")
        fobj = get_object_or_404(ParentFeedback, id=f_id)
        fobj.reply = reply_txt
        fobj.status = 1
        fobj.save()
        messages.success(request, "Reply sent.")
    return redirect("app:parent_feedback_view")

# ── EVENTS ────────────────────────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_view_events(request):
    events = Event.objects.all().order_by("-event_date")
    return render(request, "HOD/view_events.html", {"events": events})

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_add_event(request):
    if request.method == "POST":
        Event.objects.create(
            event_id=request.POST.get("event_id"),
            event_name=request.POST.get("event_name"),
            event_date=request.POST.get("event_date")
        )
        messages.success(request, "Event created.")
        return redirect("app:event")
    return render(request, "HOD/add_event.html")

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_delete_event(request, event_id):
    get_object_or_404(Event, id=event_id).delete()
    messages.success(request, "Event deleted.")
    return redirect("app:event")

# ── CLASS STATISTICS ──────────────────────────────────────────────────────────

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_class_statistics(request, class_id):
    """View class statistics with mean, median, and standard deviation for MID and EOT scores"""
    target_class = get_object_or_404(Classe, id=class_id)
    
    # Get selected term
    selected_term = request.GET.get('term', None)
    
    # Get all learners in this class
    learners = Learner.objects.filter(classe_id=target_class)
    
    # Get all subjects for this class
    subjects = Subject.objects.filter(classe_id=target_class)
    
    # Get available terms
    available_terms = AcademicRecord.objects.filter(
        learner__classe_id=target_class
    ).values_list('term', flat=True).distinct().order_by('term')
    
    # Initialize statistics
    statistics = {}
    
    if selected_term:
        # Get all records for this class and term
        records = AcademicRecord.objects.filter(
            learner__classe_id=target_class,
            term=int(selected_term)
        ).select_related('subject', 'learner')
        
        # Calculate statistics per subject
        for subject in subjects:
            subject_records = records.filter(subject=subject)
            
            if subject_records.exists():
                # Extract MID and EOT scores
                mid_scores = [r.mid for r in subject_records]
                eot_scores = [r.eot for r in subject_records]
                
                # Calculate statistics for MID
                mid_mean = sum(mid_scores) / len(mid_scores) if mid_scores else 0
                mid_sorted = sorted(mid_scores)
                mid_median = mid_sorted[len(mid_sorted) // 2] if mid_sorted else 0
                if len(mid_sorted) % 2 == 0 and len(mid_sorted) > 0:
                    mid_median = (mid_sorted[len(mid_sorted) // 2 - 1] + mid_sorted[len(mid_sorted) // 2]) / 2
                
                # Calculate standard deviation for MID
                if len(mid_scores) > 1:
                    mid_variance = sum((x - mid_mean) ** 2 for x in mid_scores) / len(mid_scores)
                    mid_std_dev = mid_variance ** 0.5
                else:
                    mid_std_dev = 0
                
                # Calculate statistics for EOT
                eot_mean = sum(eot_scores) / len(eot_scores) if eot_scores else 0
                eot_sorted = sorted(eot_scores)
                eot_median = eot_sorted[len(eot_sorted) // 2] if eot_sorted else 0
                if len(eot_sorted) % 2 == 0 and len(eot_sorted) > 0:
                    eot_median = (eot_sorted[len(eot_sorted) // 2 - 1] + eot_sorted[len(eot_sorted) // 2]) / 2
                
                # Calculate standard deviation for EOT
                if len(eot_scores) > 1:
                    eot_variance = sum((x - eot_mean) ** 2 for x in eot_scores) / len(eot_scores)
                    eot_std_dev = eot_variance ** 0.5
                else:
                    eot_std_dev = 0
                
                statistics[subject.subject_name] = {
                    'mid_mean': round(mid_mean, 2),
                    'mid_median': round(mid_median, 2),
                    'mid_std_dev': round(mid_std_dev, 2),
                    'eot_mean': round(eot_mean, 2),
                    'eot_median': round(eot_median, 2),
                    'eot_std_dev': round(eot_std_dev, 2),
                    'student_count': len(mid_scores)
                }
    
    context = {
        'target_class': target_class,
        'subjects': subjects,
        'statistics': statistics,
        'available_terms': available_terms,
        'selected_term': int(selected_term) if selected_term else None,
        'learner_count': learners.count(),
    }
    return render(request, 'HOD/class_statistics.html', context)

@login_required(login_url='app:login')
@user_passes_test(is_hod, login_url='app:login')
def hod_class_statistics(request, class_id):
    """View class statistics with mean, median, and standard deviation for MID and EOT scores"""
    target_class = get_object_or_404(Classe, id=class_id)

    # Get selected term
    selected_term = request.GET.get('term', None)

    # Get all learners in this class
    learners = Learner.objects.filter(classe_id=target_class)

    # Get all subjects for this class
    subjects = Subject.objects.filter(classe_id=target_class)

    # Get available terms
    available_terms = AcademicRecord.objects.filter(
        learner__classe_id=target_class
    ).values_list('term', flat=True).distinct().order_by('term')

    # Initialize statistics
    statistics = {}

    if selected_term:
        # Get all records for this class and term
        records = AcademicRecord.objects.filter(
            learner__classe_id=target_class,
            term=int(selected_term)
        ).select_related('subject', 'learner')

        # Calculate statistics per subject
        for subject in subjects:
            subject_records = records.filter(subject=subject)

            if subject_records.exists():
                # Extract MID and EOT scores
                mid_scores = [r.mid for r in subject_records]
                eot_scores = [r.eot for r in subject_records]

                # Calculate statistics for MID
                mid_mean = sum(mid_scores) / len(mid_scores) if mid_scores else 0
                mid_sorted = sorted(mid_scores)
                mid_median = mid_sorted[len(mid_sorted) // 2] if mid_sorted else 0
                if len(mid_sorted) % 2 == 0 and len(mid_sorted) > 0:
                    mid_median = (mid_sorted[len(mid_sorted) // 2 - 1] + mid_sorted[len(mid_sorted) // 2]) / 2

                # Calculate standard deviation for MID
                if len(mid_scores) > 1:
                    mid_variance = sum((x - mid_mean) ** 2 for x in mid_scores) / len(mid_scores)
                    mid_std_dev = mid_variance ** 0.5
                else:
                    mid_std_dev = 0

                # Calculate statistics for EOT
                eot_mean = sum(eot_scores) / len(eot_scores) if eot_scores else 0
                eot_sorted = sorted(eot_scores)
                eot_median = eot_sorted[len(eot_sorted) // 2] if eot_sorted else 0
                if len(eot_sorted) % 2 == 0 and len(eot_sorted) > 0:
                    eot_median = (eot_sorted[len(eot_sorted) // 2 - 1] + eot_sorted[len(eot_sorted) // 2]) / 2

                # Calculate standard deviation for EOT
                if len(eot_scores) > 1:
                    eot_variance = sum((x - eot_mean) ** 2 for x in eot_scores) / len(eot_scores)
                    eot_std_dev = eot_variance ** 0.5
                else:
                    eot_std_dev = 0

                statistics[subject.subject_name] = {
                    'mid_mean': round(mid_mean, 2),
                    'mid_median': round(mid_median, 2),
                    'mid_std_dev': round(mid_std_dev, 2),
                    'eot_mean': round(eot_mean, 2),
                    'eot_median': round(eot_median, 2),
                    'eot_std_dev': round(eot_std_dev, 2),
                    'student_count': len(mid_scores)
                }

    context = {
        'target_class': target_class,
        'subjects': subjects,
        'statistics': statistics,
        'available_terms': available_terms,
        'selected_term': int(selected_term) if selected_term else None,
        'learner_count': learners.count(),
    }
    return render(request, 'HOD/class_statistics.html', context)

