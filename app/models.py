from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.timezone import now

# 1. AUTHENTICATION MODEL
class CustomUser(AbstractUser):
    USER_TYPES = (
        ("1", "ADMIN"),
        ("2", "TEACHER"),
        ("3", "PARENT"),
    )
    user_type = models.CharField(choices=USER_TYPES, max_length=50, default="1")
    profile_pic = models.ImageField(upload_to="profile_pic", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

# 2. INFRASTRUCTURE MODELS
class SessionYear(models.Model):
    session_start = models.CharField(max_length=100)
    session_end = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.session_start} - {self.session_end}"

class Classe(models.Model):
    CLASS_CHOICES = [
        ("P1", "Primary One"), ("P2", "Primary Two"), ("P3", "Primary Three"),
        ("P4", "Primary Four"), ("P5", "Primary Five"), ("P6", "Primary Six"), ("P7", "Primary Seven"),
    ]
    class_name = models.CharField(max_length=3, choices=CLASS_CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_class_name_display()

# 3. PROFILE MODELS (The "Links")
class Teacher(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    teacher_id = models.CharField(max_length=50, unique=True)
    teacher_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=(("M", "Male"), ("F", "Female")))
    qualification = models.CharField(max_length=100)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f": {self.admin.first_name} {self.admin.last_name}"

class Parent(models.Model):
    # Link to Login Account
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    parent_id = models.CharField(max_length=50, unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f": {self.admin.first_name} {self.admin.last_name}"

class Learner(models.Model):
    # 1. Links to other tables
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    classe_id = models.ForeignKey(Classe, on_delete=models.CASCADE)
    session_year_id = models.ForeignKey(SessionYear, on_delete=models.CASCADE, null=True, blank=True)

    # 2. Personal Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    learner_id = models.CharField(max_length=20, unique=True)
    gender = models.CharField(max_length=1, choices=[("F", "Female"), ("M", "Male")])
    date_of_birth = models.DateField(null=True, blank=True)
    religion = models.CharField(max_length=2, choices=[
        ("C", "Catholic"), ("A", "Anglican"), ("M", "Muslim"),
        ("S", "Seventh Day"), ("BA", "Born Again"), ("O", "Other")
    ])
    nationality = models.CharField(max_length=50, default="Ugandan")

    # 3. Enrollment Details
    section = models.CharField(max_length=1, choices=[("D", "Day"), ("B", "Boarding")])
    health_issue = models.CharField(max_length=255, blank=True, null=True)
    relationship_with_learner = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name='children')
    parent_mobile_number = models.CharField(max_length=15, null=True, blank=True)
    present_address = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.learner_id})"

    # Add the get_age method here
    def get_age(self):
        if self.date_of_birth:
            today = now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return "N/A"

# 4. ACADEMIC MODELS
class Subject(models.Model):
    subject_name = models.CharField(max_length=100)
    classe_id = models.ForeignKey(Classe, on_delete=models.CASCADE)
    staff = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.subject_name} ({self.classe_id})"

class AcademicRecord(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    term = models.IntegerField(choices=[(1, "Term 1"), (2, "Term 2"), (3, "Term 3")])
    mid = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    eot = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    final_weighted_mark = models.FloatField(editable=False, default=0)
    score = models.CharField(max_length=5, editable=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.final_weighted_mark = (self.mid * 0.5) + (self.eot * 0.5)
        mark = self.final_weighted_mark
        if mark >= 90: self.score = "D1"
        elif mark >= 80: self.score = "D2"
        elif mark >= 70: self.score = "C3"
        elif mark >= 60: self.score = "C4"
        elif mark >= 55: self.score = "C5"
        elif mark >= 50: self.score = "C6"
        elif mark >= 45: self.score = "P7"
        elif mark >= 40: self.score = "P8"
        else: self.score = "F9"
        super().save(*args, **kwargs)

class TermSummary(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE)
    term = models.IntegerField(choices=[(1, "Term 1"), (2, "Term 2"), (3, "Term 3")])
    days_present = models.IntegerField(default=0)
    days_absent = models.IntegerField(default=0)
    teacher_comment = models.TextField(blank=True, null=True)
    headteacher_remark = models.CharField(max_length=200, default="Promising. Keep up the struggle.")

    def __str__(self):
        return f"Report Summary: {self.learner.admin.first_name} - T{self.term}"

class parent_notification(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.parent_id.admin.first_name}"

class parent_feedback(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField(blank=True, null=True)
    status = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.parent_id.admin.first_name}"

class staff_notification(models.Model):
    staff_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    message = models.TextField()
    status = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.staff_id.admin.first_name}"

class staff_feedback(models.Model):
    staff_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField(blank=True, null=True)
    status = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.staff_id.admin.first_name}"