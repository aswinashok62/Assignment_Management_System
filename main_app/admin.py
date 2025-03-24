from django.contrib import admin

from .models import Teacher, Program, Course, StudentApproval

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'email', 'phone', 'department', 'date_of_joining')
    filter_horizontal = ('courses_assigned',)  # To manage many-to-many field in admin

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_name', 'program_code', 'duration', 'description')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('course_name', 'course_code', 'program', 'credits', 'semester', 'teacher')


class StudentApprovalAdmin(admin.ModelAdmin):
    list_display = ('student', 'is_approved')  # Show student and approval status
    list_filter = ('is_approved',)             # Filter by approval status (True/False)
    search_fields = ('student__username',)     # Search by student username

admin.site.register(StudentApproval, StudentApprovalAdmin)


