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
        ("4", "HOD"),
    )
    user_type = models.CharField(choices=USER_TYPES, max_length=50, default="1")
    profile_pic = models.ImageField(upload_to="profile_pic", null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.username})"

    @property
    def can_access_hod(self):
        return self.user_type in ['1', '4'] or self.is_superuser

    @property
    def can_access_staff(self):
        # Staff door is closed for HODs to avoid navigation confusion
        try:
            return (hasattr(self, 'staff') or self.user_type == '2') and self.user_type != '4'
        except:
            return False

    @property
    def can_access_parent(self):
        # A user can access parent portal if they have a Parent profile link
        try:
            return hasattr(self, 'parent') or self.user_type == '3'
        except:
            return False

    class Meta:
        db_table = 'Users'

# 2. INFRASTRUCTURE MODELS
class SessionYear(models.Model):
    session_start = models.CharField(max_length=100)
    session_end = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.session_start} - {self.session_end}"
    class Meta:
        db_table =  "Session_Year "



class Classe(models.Model):
    CLASS_CHOICES = [
        ("P1", "Primary One"), ("P2", "Primary Two"), ("P3", "Primary Three"),
        ("P4", "Primary Four"), ("P5", "Primary Five"), ("P6", "Primary Six"), ("P7", "Primary Seven"),
    ]
    class_name = models.CharField(max_length=3, choices=CLASS_CHOICES, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.get_class_name_display()
    class Meta:
        db_table = 'Class'

class Staff(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    staff_id = models.CharField(max_length=20, unique=True)
    staff_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female')))
    qualification = models.CharField(max_length=100)
    address = models.TextField()
    subject_name = models.CharField(max_length=100, null=True, blank=True, default="")
    class_name = models.CharField(max_length=50, null=True, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "staff"
        verbose_name_plural = "staff"

    def __str__(self):
        return self.staff_name
    class Meta:
        db_table = 'Staff'

class Parent(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    parent_id = models.CharField(max_length=50,unique=True)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.parent_name} ({self.parent_id})"
    class Meta:
        db_table = 'Parent'

class Learner(models.Model):
    school_class = models.ForeignKey(Classe, on_delete=models.CASCADE, db_column='class_id', verbose_name="class_name")
    session_year = models.ForeignKey(SessionYear, on_delete=models.CASCADE, null=True, blank=True, db_column='session_year_id')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    learner_id = models.CharField(max_length=20,unique=True)
    gender = models.CharField(max_length=1, choices=[("F", "Female"), ("M", "Male")])
    date_of_birth = models.DateField(null=True, blank=True)
    religion = models.CharField(max_length=2, choices=[
        ("C", "Catholic"), ("A", "Anglican"), ("M", "Muslim"),
        ("S", "Seventh Day"), ("BA", "Born Again"), ("O", "Other")
    ])
    nationality = models.CharField(max_length=50, default="Ugandan")
    section = models.CharField(max_length=1, choices=[("D", "Day"), ("B", "Boarding")])
    health_issue = models.CharField(max_length=255, blank=True, null=True)
    relationship_with_learner = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey(Parent, on_delete=models.SET_NULL, null=True, blank=True, related_name='children', to_field='parent_id')
    parent_mobile_number = models.CharField(max_length=15, null=True, blank=True)
    
   
    fees_paid = models.BooleanField(default=False, help_text="Set to Yes when all school fees are cleared")

    class Meta:
        ordering = ['learner_id']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.learner_id})"

    def save(self, *args, **kwargs):
        
        if self.pk:
            try:
                old_instance = Learner.objects.get(pk=self.pk)
                if old_instance.learner_id != self.learner_id:
                    from django.db import transaction
                    from django.apps import apps
                    AcademicRecord = apps.get_model('app', 'AcademicRecord')
                    TermSummary = apps.get_model('app', 'TermSummary')
                    with transaction.atomic():
                        AcademicRecord.objects.filter(learner=old_instance.learner_id).update(learner=self.learner_id)
                        TermSummary.objects.filter(learner=old_instance.learner_id).update(learner=self.learner_id)
                        super().save(*args, **kwargs)
                    return
            except Learner.DoesNotExist:
                pass
        super().save(*args, **kwargs)

    
    def get_age(self):
        if self.date_of_birth:
            today = now().date()
            return today.year - self.date_of_birth.year - (
                (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day)
            )
        return "N/A"
    class Meta:
        db_table = 'Learner'
# 4. ACADEMIC MODELS
class Subject(models.Model):
    subject_id = models.CharField(max_length=50, unique=True)
    subject_name = models.CharField(max_length=100)
    class_id = models.ForeignKey(Classe, on_delete=models.CASCADE, db_column='class_id', verbose_name="class_name")
    staff = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, to_field='staff_id')

    def __str__(self):
        return f"{self.subject_name} ({self.class_id})"
    class Meta:
        db_table = 'Subject'

class AcademicRecord(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, to_field='learner_id')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, to_field='subject_id')
    term = models.IntegerField(choices=[(1, "Term 1"), (2, "Term 2"), (3, "Term 3")])
    mid = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    eot = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    final_weighted_mark = models.FloatField(editable=False, default=0)
    score = models.CharField(max_length=2, editable=False, null=True, blank=True)

    class Meta:
        unique_together = ('learner', 'subject', 'term')

    def get_score_color(self):
        """Returns the hex color code associated with the grade score"""
        colors = {
            'D1': '#2e7d32', 'D2': '#2e7d32',
            'C3': '#1976d2', 'C4': '#1976d2', 'C5': '#1976d2', 'C6': '#1976d2',
            'P7': '#f57c00', 'P8': '#f57c00',
            'F9': '#c62828'
        }
        return colors.get(self.score, '#333333')

    def get_remark(self):
        """Returns readable remark based on score"""
        remarks = {
            'D1': 'Distinction 1 (Excellent)',
            'D2': 'Distinction 2 (Very Good)',
            'C3': 'Credit 3 (Good)',
            'C4': 'Credit 4 (Satisfactory)',
            'C5': 'Credit 5 (Fair)',
            'C6': 'Credit 6 (Pass)',
            'P7': 'Pass 7 (Weak)',
            'P8': 'Pass 8 (Very Weak)',
            'F9': 'Fail 9 (Failed)'
        }
        return remarks.get(self.score, 'N/A')

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
    class Meta:
        db_table = 'AcademicRecord'

class TermSummary(models.Model):
    learner = models.ForeignKey(Learner, on_delete=models.CASCADE, to_field='learner_id')
    term = models.IntegerField(choices=[(1, "Term 1"), (2, "Term 2"), (3, "Term 3")], default=1, null=True, blank=True)
    total_marks = models.FloatField(default=0, null=True, blank=True)
    average = models.FloatField(default=0, null=True, blank=True)
    position = models.IntegerField(null=True, blank=True)
    total_learners = models.IntegerField(null=True, blank=True)
    teacher_comment = models.TextField(null=True, blank=True, default="")
    headteacher_remark = models.TextField(null=True, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('learner', 'term')
        permissions = [
            ("can_view_report_card", "Can View Report Card"),
        ]

    def __str__(self):
        return f"Summary: {self.learner.first_name} - Term {self.term}"
    class Meta:
        db_table = 'TermSummary'


            

class parent_notification(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE, db_column='parent_id')
    message = models.TextField()
    status = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.parent_id.admin.first_name}"
    class Meta:
        db_table = 'parent_notification'
class parent_feedback(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE, db_column='parent_id')
    feedback = models.TextField()
    reply = models.TextField(blank=True, null=True)
    status = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.parent_id.admin.first_name}"
    class Meta:
        db_table = 'parent_feedback'
class staff_notification(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, to_field='staff_id', db_column='staff_id')
    message = models.TextField()
    status = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.staff_id.staff_name}"
    class Meta:
        db_table = 'staff_notification'
class staff_feedback(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, to_field='staff_id', db_column='staff_id')
    feedback = models.TextField()
    reply = models.TextField(blank=True, null=True)
    status = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.staff_id.staff_name}"
    class Meta:
        db_table = 'staff_feedback'


