from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from app.models import (
    Learner,
    Teacher,
    Classe,
    Subject,
    SessionYear,
    Parent,
    parent_notification,
    staff_notification,
)


ParentNotification = parent_notification
StaffNotification = staff_notification


def is_admin(user):
    
    return getattr(user, "user_type", "") == "1" and user.is_authenticated


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def HOME(request):
    context = {
        "learner_count": Learner.objects.count(),
        "staff_count": Teacher.objects.count(),
        "subject_count": Subject.objects.count(),
        "learner_gender_female": Learner.objects.filter(gender="F").count(),
        "learner_gender_male": Learner.objects.filter(gender="M").count(),
    }
    return render(request, "Admin/home.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def add_learner(request):
    sessions = SessionYear.objects.all()
    classes = Classe.objects.all()

    if request.method == "POST":
        messages.info(
            request,
            "Learner creation is not implemented. To enable creation please provide "
            "username/email/password fields or ask me to implement the create flow."
        )
        return redirect("add_learner")

    return render(request, "Admin/add_learner.html", {"sessions": sessions, "classe": classes})


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def view_learners(request):
    learners = Learner.objects.select_related("admin", "parent__admin", "classe_id", "session_year_id").all()
    return render(request, "Admin/view_learners.html", {"learners": learners})


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def add_session(request):
    if request.method == "POST":
        start = request.POST.get("session_year_start")
        end = request.POST.get("session_year_end")
        if start and end:
            SessionYear.objects.create(session_start=start, session_end=end)
            messages.success(request, "Session created successfully!")
            return redirect("add_session")
        messages.error(request, "Start and end year are required.")
    return render(request, "Admin/add_session.html")


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def view_session(request):
    sessions = SessionYear.objects.all()
    return render(request, "Admin/view_session.html", {"session": sessions})


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def add_event(request):
    return render(request, "Admin/add_event.html")


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def class_broadsheet(request, class_id):
    target_class = get_object_or_404(Classe, id=class_id)
    learners = Learner.objects.filter(classe_id=target_class).select_related("admin", "session_year_id")
    return render(request, "Admin/broadsheet.html", {"class_name": target_class.class_name, "learners": learners})


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def view_parent(request):
    parents = Parent.objects.select_related("admin").all()
    return render(request, "Admin/view_parent.html", {"parents": parents})




@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def send_staff_notification(request):
    staff_members = Teacher.objects.select_related("admin").all()
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        message_text = request.POST.get("message")
        if not staff_id or not message_text:
            messages.error(request, "Please select a staff member and provide a message.")
            return redirect("add_staff_notification")

        staff_obj = get_object_or_404(Teacher, id=staff_id)
        StaffNotification.objects.create(staff_id=staff_obj, message=message_text)
        messages.success(request, "Notification sent to staff!")
        return redirect("add_staff_notification")

    return render(request, "Admin/staff_notification.html", {"staff": staff_members})


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def send_parent_notification(request):
    parents = Parent.objects.select_related("admin").all()
    if request.method == "POST":
        parent_id = request.POST.get("parent_id")
        message_text = request.POST.get("message")
        if not parent_id or not message_text:
            messages.error(request, "Please select a parent and provide a message.")
            return redirect("add_parent_notification")

        parent_obj = get_object_or_404(Parent, id=parent_id)
        ParentNotification.objects.create(parent_id=parent_obj, message=message_text)
        messages.success(request, "Notification sent to the parent!")
        return redirect("add_parent_notification")

    return render(request, "Admin/parent_notification.html", {"parents": parents})


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def staff_notification_mark_done(request, notification_id):
    notification = get_object_or_404(StaffNotification, id=notification_id)
    notification.status = 1
    notification.save()
    return redirect("add_staff_notification")


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def parent_notification_mark_done(request, notification_id):
    notification = get_object_or_404(ParentNotification, id=notification_id)
    notification.status = 1
    notification.save()
    return redirect("add_parent_notification")




@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def update_learner(request, learner_id):
    learner = get_object_or_404(Learner, id=learner_id)

    if request.method == "POST":
       
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        if first_name:
            learner.admin.first_name = first_name
        if last_name:
            learner.admin.last_name = last_name

       
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
            except Exception:
                
                pass

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

        learner.parent_mobile_number = request.POST.get("parent_mobile_number", learner.parent_mobile_number)

        learner.save()
        messages.success(request, "Learner updated successfully.")
        return redirect("view_learners")

    context = {
        "learner": learner,
        "classe": Classe.objects.all(),
        "session_year": SessionYear.objects.all(),
        "parents": Parent.objects.all(),
    }
   
    return render(request, "Admin/update_learner.html", context)


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def update_session(request, session_id):
    session = get_object_or_404(SessionYear, id=session_id)
    if request.method == "POST":
        start = request.POST.get("session_year_start")
        end = request.POST.get("session_year_end")
        if start and end:
            session.session_start = start
            session.session_end = end
            session.save()
            messages.success(request, "Session updated.")
            return redirect("view_session")
        messages.error(request, "Start and end dates are required.")
        return redirect("update_session", session_id=session.id)
    return render(request, "Admin/update_session.html", {"session": session})


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def update_staff(request, staff_id):
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
        
        if hasattr(staff, "address"):
            staff.address = request.POST.get("address", getattr(staff, "address", ""))

        
        staff.teacher_name = f"{staff.admin.first_name} {staff.admin.last_name}"

        staff.save()
        messages.success(request, "Teacher updated.")
        return redirect("view_staff")

    return render(request, "Admin/update_staff.html", {"staff": staff})


@login_required(login_url="/login/")
@user_passes_test(is_admin, login_url="/login/")
def update_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == "POST":
        subject.subject_name = request.POST.get("subject_name", subject.subject_name)

        classe_id = request.POST.get("classe_id")
        if classe_id:
            subject.classe_id = get_object_or_404(Classe, id=classe_id)

        staff_id = request.POST.get("staff_id")
        if staff_id:
            subject.staff = get_object_or_404(Teacher, id=staff_id)
        else:
            subject.staff = None

        
        if "link" in request.POST and hasattr(subject, "link"):
            subject.link = request.POST.get("link", getattr(subject, "link", ""))

        subject.save()
        messages.success(request, "Subject updated.")
        return redirect("view_subject")

    context = {
        "subject": subject,
        "classe": Classe.objects.all(),
        "staff": Teacher.objects.select_related("admin").all(),
    }
    return render(request, "Admin/update_subject.html", context)