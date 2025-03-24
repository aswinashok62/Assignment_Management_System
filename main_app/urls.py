from django.urls import path
from . import views
from .views import add_teacher,delete_assignment, edit_assignment,delete_submission,teacher_students
from .views import add_program,program_list,delete_program,update_program,add_course,view_courses,edit_course,delete_course,admin_login,create_assignment,scheduled_assignments


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/edit/<int:id>/', views.edit_teacher, name='edit_teacher'),  # Edit Teacher
    path('teachers/delete/<int:id>/', views.delete_teacher, name='delete_teacher'),  # Delete Teacher
    path('add-program/', add_program, name='add_program'),
    path('program-list/', program_list, name='program_list'),
    #path("delete-program/<int:program_id>/", delete_program, name="delete_program"),
    path('delete-program/<int:program_id>/', views.delete_program, name='delete_program'),
    path("update-program/<int:program_id>/", update_program, name="update_program"),
    path('courses/add/', add_course, name='add_course'),
    path('courses/', view_courses, name='view_courses'),
     path('courses/edit/<int:course_id>/', edit_course, name='edit_course'),
    path('courses/delete/<int:course_id>/', delete_course, name='delete_course'),
    #path('logout/', logout_view, name='logout'),
    #path('logout/', LogoutView.as_view(), name='logout'),
     #admin login
    path('login/', admin_login, name='admin_login'),

    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),

    path('teacher/assignment/create/', create_assignment, name='create_assignment'),
    path('assignments/scheduled/', scheduled_assignments, name='scheduled_assignments'),
    #path('teacher/assignment/delete/<int:assignment_id>/', views.delete_assignment, name='delete_assignment'),
    #path('teacher/submissions/', views.teacher_view_submissions, name='teacher_view_submissions'),
    #path('teacher/add-remark/<int:submission_id>/', views.add_remark, name='add_remark'),
    path('teacher/submissions/', views.teacher_view_submissions, name='teacher_view_submissions'),
    path('teacher/add-remark/<int:submission_id>/', views.add_remark, name='add_remark'),
    path('register/', views.student_register, name='student_register'),
    path('logins/', views.student_login, name='student_login'),
    path('dashboards/', views.student_dashboard, name='student_dashboard'),
    path('assignments/<int:course_id>/', views.assignment_list, name='assignment_list'),
    path('assignment/<int:assignment_id>/', views.assignment_detail, name='assignment_detail'),
    #path('course/<int:course_id>/assignments/', views.assignment_list, name='assignment_list'),
    path('assignment/<int:assignment_id>/upload/', views.upload_assignment, name='upload_assignment'),  # URL for assignment upload
    #path('student/remarks/', views.student_view_remarks, name='student_view_remarks'),
    path('student/remarks/', views.student_view_remarks, name='student_view_remarks'),
    #path('student/performance-chart/', views.student_performance_chart, name='student_performance_chart'),
    path('student/performance-chart/', views.student_performance_chart, name='student_performance_chart'),
    #path('manage-students/', views.manage_student_approval, name='manage_student_approval'),
    path('manage-students/', views.manage_student_approval, name='manage_student_approval'),
    path('profile/', views.student_profile, name='student_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('assignment/delete/<int:assignment_id>/', delete_assignment, name='delete_assignment'),
    #path('assignment/edit/<int:assignment_id>/', edit_assignment, name='edit_assignment'),
    path('delete-submission/<int:submission_id>/', delete_submission, name='delete_submission'),
    path("delete-submission/<int:submission_id>/", views.delete_submission, name="delete_submission"),
    path('assignment/<int:assignment_id>/edit/', edit_assignment, name='edit_assignment'),
    #path('teacher/<int:teacher_id>/students/', teacher_students, name='teacher_students'),
    #path('teacher/students/', teacher_students, name='teacher_students'),
    #path('teacher/<int:teacher_id>/students/', teacher_students, name='teacher_students'),
    path('teacher/<int:teacher_id>/students/', views.teacher_students, name='teacher_students'),

]
    



