from django.urls import path
from . import views
from . import Admin_Views, Staff_Views, Parent_Views

app_name = "app"

urlpatterns = [
    # Authentication
    path('login/', views.login_page, name='login'),
    path('do-login/', views.doLogin, name='do_login'),
    path('logout/', views.doLogout, name='logout'),

    # Admin (custom dashboards)
    path('admin-dashboard/', Admin_Views.HOME, name='admin_dashboard'),
    path('admin/learners/', Admin_Views.view_learners, name='view_learners'),
    path('admin/add-session/', Admin_Views.add_session, name='add_session'),
    path('admin/send-staff-notification/', Admin_Views.send_staff_notification, name='add_staff_notification'),
    path('admin/send-parent-notification/', Admin_Views.send_parent_notification, name='add_parent_notification'),
    path('admin/learner/<int:learner_id>/update/', Admin_Views.update_learner, name='update_learner'),
    path('admin/session/<int:session_id>/update/', Admin_Views.update_session, name='update_session'),
    path('admin/staff/<int:staff_id>/update/', Admin_Views.update_staff, name='update_staff'),
    path('admin/subject/<int:subject_id>/update/', Admin_Views.update_subject, name='update_subject'),

    path('Staff/home/', Staff_Views.teacher_home, name='teacher_home'),
    path('Staff/upload-marks/', Staff_Views.upload_marks_csv, name='upload_marks'),
    path('Staff/notifications/', Staff_Views.staff_notifications_all, name='staff_notifications'),
    path('Staff/feedback/', Staff_Views.staff_feedback_save, name='staff_feedback'),


    path('Parent/home/', Parent_Views.parent_dashboard, name='parent_dashboard'),
    path('Parent/report/<int:learner_id>/', Parent_Views.view_report_card, name='view_report_card'),
    path('Parent/notifications/', Parent_Views.parent_notifications_all, name='parent_notifications'),
    path('Parent/feedback/', Parent_Views.parent_feedback_save, name='parent_feedback'),
]