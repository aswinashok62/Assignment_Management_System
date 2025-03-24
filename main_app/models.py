from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


# Teacher Model
class Teacher(models.Model):
   
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)  # Unique Employee ID
    email = models.EmailField(unique=True)
    phone_validator = RegexValidator(
        regex=r'^\d{10}$',
        message="Phone number must be exactly 10 digits."
    )
    phone = models.CharField(
        max_length=10, 
        validators=[phone_validator], 
        unique=True,  # Ensuring unique phone numbers
        blank=True, 
        null=True
    )
    department = models.CharField(max_length=100)
    courses_assigned = models.ManyToManyField('Course', blank=True, related_name="assigned_teachers")  # Many-to-Many relationship
    qualification = models.CharField(max_length=200)
    date_of_joining = models.DateField()

    def __str__(self):
        return self.name

# Program Model
class Program(models.Model):
    program_name = models.CharField(max_length=100)
    program_code = models.CharField(max_length=20, unique=True)  # Unique Program Code
    duration = models.IntegerField(help_text="Duration in years")  # Duration in years
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.program_name

# Course Model
class Course(models.Model):
    course_name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)  # Unique Course Code
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="courses")  # Linked to Program
    credits = models.IntegerField(default=3)  # Credit Hours
    semester = models.IntegerField(help_text="Semester number")
    description = models.TextField(blank=True, null=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name="courses_taught")  # Optional

    def __str__(self):
        return self.course_name
    
from django.core.validators import FileExtensionValidator

class Assignment(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="assignments")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="assignments")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="assignments")
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateField()
    file = models.FileField(
        upload_to="assignments/",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]  # Restrict to PDFs only
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return self.title

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Linking student to the User model for login
    name = models.CharField(max_length=100)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)  # Linking to Program
    course = models.ForeignKey(Course, on_delete=models.CASCADE)  # Linking to Course
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_assignments(self):
        # Fetching assignments related to the student's enrolled program and course
        return Assignment.objects.filter(course=self.course)
    
class AssignmentSubmission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="submissions")
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name="submissions")
    file = models.FileField(
        upload_to="submissions/",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    submitted_at = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=10, blank=True, null=True)  # Optional field for grading
    gained_marks = models.PositiveIntegerField(blank=True, null=True)
    max_marks = models.PositiveIntegerField(blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Submission by {self.student.name} for {self.assignment.title}"

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    

class StudentApproval(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.username} - {'Approved' if self.is_approved else 'Pending/Rejected'}"    

