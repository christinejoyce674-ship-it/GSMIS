from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CustomUser, Classe, Teacher, Parent, Learner,
    Subject, AcademicRecord, staff_notification,
    parent_feedback, staff_feedback, parent_notification, SessionYear
)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('user_type', 'profile_pic')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('user_type', 'profile_pic')}),
    )

@admin.register(Learner)
class LearnerAdmin(admin.ModelAdmin):
    list_display = ('learner_id', 'first_name', 'last_name', 'classe_id', 'gender', 'get_age', 'section')
    list_filter = ('classe_id', 'gender', 'section', 'religion')
    search_fields = ('first_name', 'last_name', 'learner_id')
    autocomplete_fields = ['admin', 'parent', 'classe_id']

    def get_age(self, obj):
        return obj.get_age()
    get_age.short_description = 'Age'

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    search_fields = ('subject_name',)
    list_display = ('subject_name', 'classe_id')

@admin.register(SessionYear)
class SessionYearAdmin(admin.ModelAdmin):
    list_display = ('session_start', 'session_end')
    search_fields = ('session_start', 'session_end')

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('class_name',)
    search_fields = ('class_name',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'teacher_name', 'gender', 'qualification', 'admin')
    search_fields = ('admin__first_name', 'admin__last_name', 'teacher_id')
    autocomplete_fields = ['admin']

@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ('admin', 'parent_id')
    search_fields = ('admin__first_name', 'admin__last_name', 'parent_id')
    autocomplete_fields = ['admin']

@admin.register(AcademicRecord)
class AcademicRecordAdmin(admin.ModelAdmin):
    autocomplete_fields = ['learner', 'subject']
    list_display = ('learner', 'subject', 'term', 'mid', 'eot', 'final_weighted_mark', 'score')
    list_filter = ('term', 'subject', 'learner__classe_id')
    search_fields = ('learner__admin__first_name', 'learner__admin__last_name')

    def get_total(self, obj):
        return (obj.mid or 0) + (obj.eot or 0)
    get_total.short_description = 'Total'

    def get_grade(self, obj):
        total = self.get_total(obj)
        if total >= 90: return "D1"
        elif total >= 80: return "D2"
        elif total >= 70: return "C3"
        elif total >= 60: return "C4"
        elif total >= 55: return "C5"
        elif total >= 50: return "C6"
        elif total >= 45: return "P7"
        elif total >= 40: return "P8"
        else: return "F9"
    get_grade.short_description = 'Grade'

# Notifications & feedback models
admin.site.register(staff_notification)
admin.site.register(staff_feedback)
admin.site.register(parent_notification)
admin.site.register(parent_feedback)
admin.site.register(parent_feedback)
