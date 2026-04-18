from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.db.models import Avg
from .models import (
    CustomUser, Classe, Teacher, Parent, Learner,
    Subject, AcademicRecord, staff_notification,
    parent_feedback, staff_feedback, parent_notification, SessionYear, TermSummary
)

admin.site.site_header = "Good Hope Nabulagala Management Information System"
admin.site.index_title = "School Administration Dashboard"


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
    list_display = ('learner_id', 'first_name', 'last_name', 'classe_id', 'gender', 'get_age', 'section', 'fees_paid')
    list_filter = ('classe_id', 'gender', 'section', 'religion', 'fees_paid')
    search_fields = ('first_name', 'last_name', 'learner_id')
    autocomplete_fields = ['admin', 'parent', 'classe_id']
    list_editable = ('fees_paid',)

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


@admin.register(TermSummary)
class TermSummaryAdmin(admin.ModelAdmin):
    list_display = ('learner', 'term', 'days_present', 'days_absent', 'teacher_comment', 'headteacher_remark')
    list_filter = ('term',)
    search_fields = ('learner__first_name', 'learner__last_name')


# Notifications & feedback models
admin.site.register(staff_notification)
admin.site.register(staff_feedback)
admin.site.register(parent_notification)
admin.site.register(parent_feedback)
