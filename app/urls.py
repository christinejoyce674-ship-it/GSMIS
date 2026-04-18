from django.urls import path
from . import views
from . import Staff_Views, Parent_Views, HOD_Views

app_name = "app"

urlpatterns = [
    # ── Authentication ────────────────────────────────────────────────────────
    path('', views.landing, name='landing'),
    path('login/', views.login_page, name='login'),
    path('doLogin/', views.doLogin, name='doLogin'),
    path('doLogout/', views.logout, name='logout'),

    # ── HOD (Head Teacher) Management ─────────────────────────────────────────
    path('hod/', HOD_Views.hod_home, name='hod_home'),
    path('admin-panel/', HOD_Views.hod_home, name='home'), # Backward compatibility

    # Learners
    path('hod/learners/', HOD_Views.hod_view_learners, name='view_learners'),
    path('hod/learners/add/', HOD_Views.hod_add_learner, name='add_learner'),
    path('hod/learner/<int:learner_id>/update/', HOD_Views.hod_update_learner, name='update_learner'),
    path('hod/learner/<int:learner_id>/delete/', HOD_Views.hod_delete_learner, name='delete_learner'),
    path('hod/learner/<int:learner_id>/report/', HOD_Views.hod_view_learner_report, name='hod_learner_report'),
    path('hod/learner/<int:learner_id>/term/<int:term>/remarks/', HOD_Views.hod_update_term_summary, name='hod_term_summary'),
    path('hod/learner/<int:learner_id>/fees/', HOD_Views.hod_toggle_fees, name='hod_toggle_fees'),

    # Staff
    path('hod/staff/', HOD_Views.hod_view_staff, name='view_staff'),
    path('hod/staff/add/', HOD_Views.hod_add_staff, name='add_staff'),
    path('hod/staff/<int:staff_id>/update/', HOD_Views.hod_update_staff, name='update_staff'),
    path('hod/staff/<int:staff_id>/delete/', HOD_Views.hod_delete_staff, name='delete_staff'),
    path('hod/staff/<int:staff_id>/promote/', HOD_Views.hod_promote_staff, name='promote_staff'),

    # Parents
    path('hod/parents/', HOD_Views.hod_view_parent, name='view_parent'),
    path('hod/parents/add/', HOD_Views.hod_add_parent, name='add_parent'),
    path('hod/parent/<int:parent_id>/update/', HOD_Views.hod_update_parent, name='update_parent'),
    path('hod/parent/<int:parent_id>/delete/', HOD_Views.hod_delete_parent, name='delete_parent'),

    # Classes
    path('hod/classes/', HOD_Views.hod_view_class, name='view_class'),
    path('hod/classes/add/', HOD_Views.hod_add_class, name='add_class'),
    path('hod/class/<int:class_id>/update/', HOD_Views.hod_update_class, name='update_class'),
    path('hod/class/<int:class_id>/delete/', HOD_Views.hod_delete_class, name='delete_class'),

    # Subjects
    path('hod/subjects/', HOD_Views.hod_view_subject, name='view_subject'),
    path('hod/subjects/add/', HOD_Views.hod_add_subject, name='add_subject'),
    path('hod/subject/<int:subject_id>/update/', HOD_Views.hod_update_subject, name='update_subject'),
    path('hod/subject/<int:subject_id>/delete/', HOD_Views.hod_delete_subject, name='delete_subject'),

    # Sessions
    path('hod/sessions/', HOD_Views.hod_view_session, name='view_session'),
    path('hod/sessions/add/', HOD_Views.hod_add_session, name='add_session'),
    path('hod/session/<int:session_id>/update/', HOD_Views.hod_update_session, name='update_session'),
    path('hod/session/<int:session_id>/delete/', HOD_Views.hod_delete_session, name='delete_session'),

    # Notifications
    path('hod/send-staff-notification/', HOD_Views.hod_send_staff_notification, name='add_staff_notification'),
    path('hod/send-parent-notification/', HOD_Views.hod_send_parent_notification, name='add_parent_notification'),
    # Note: done marks might need refactoring if they were in Admin_Views
    
    # Events
    path('hod/events/', HOD_Views.hod_view_events, name='event'),
    path('hod/events/add/', HOD_Views.hod_add_event, name='addevent'),
    path('hod/events/delete/<int:event_id>/', HOD_Views.hod_delete_event, name='delete_event'),

    # Feedback Replies
    path('hod/staff-feedback/', HOD_Views.hod_staff_feedback_view, name='staff_feedback_view'),
    path('hod/parent-feedback/', HOD_Views.hod_parent_feedback_view, name='parent_feedback_view'),
    path('hod/staff-feedback/reply/', HOD_Views.hod_staff_feedback_reply, name='staff_feedback_reply'),
    path('hod/parent-feedback/reply/', HOD_Views.hod_parent_feedback_reply, name='parent_feedback_reply'),

    # Broadsheet
    path('hod/broadsheet/<int:class_id>/', HOD_Views.hod_broadsheet, name='hod_broadsheet'),
    
    # Class Statistics
    path('hod/class/<int:class_id>/statistics/', HOD_Views.hod_class_statistics, name='hod_class_statistics'),

    # ── Staff / Teacher ───────────────────────────────────────────────────────
    path('staff/teacher-home/', Staff_Views.teacher_home, name='teacher_home'),
    path('staff/upload-marks/<int:classe_id>/', Staff_Views.upload_marks_csv, name='upload_marks'),
    path('staff/notifications/', Staff_Views.staff_notifications_all, name='staff_notifications'),
    path('staff/feedback/', Staff_Views.staff_feedback_save, name='staff_feedback'),
    path('staff/feedback/save/', Staff_Views.staff_feedback_save, name='staff_feedback_save'),

    # ── Parent ────────────────────────────────────────────────────────────────
    path('parent/dashboard/', Parent_Views.parent_dashboard, name='parent_dashboard'),
    path('parent/report/<int:learner_id>/', Parent_Views.view_report_card, name='view_report_card'),
    path('parent/midterm-report/<int:learner_id>/', Parent_Views.view_midterm_report, name='view_midterm_report'),
    path('parent/notifications/', Parent_Views.parent_notifications_all, name='parent_notifications'),
    path('parent/feedback/', Parent_Views.parent_feedback_view, name='parent_feedback'),
]
