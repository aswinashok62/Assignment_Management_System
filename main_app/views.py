from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Teacher, Program, Course,Assignment,Student,AssignmentSubmission,StudentApproval
from .forms import TeacherForm,CourseForm,TeacherLoginForm,AssignmentForm,StudentLoginForm,AssignmentUploadForm,StudentUpdateForm
from .forms import ProgramForm,AssignmentRemarkForm
from django.http import JsonResponse
from django.contrib import messages
#from django.contrib.auth import logout
from django.contrib.auth.models import User
from .forms import StudentRegistrationForm,EditAssignmentForm
from datetime import datetime
from django.utils.timezone import localdate,now
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'main_app/home.html')



def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Ensures only admins can log in
            login(request, user)
            return redirect('admin_dashboard')  # Redirect to admin dashboard
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'main_app/admin_login.html')


def admin_dashboard(request):
    # Fetch the counts of each entity
    teacher_count = Teacher.objects.count()
    program_count = Program.objects.count()
    course_count = Course.objects.count()
    student_count = Student.objects.count()

    # Pass counts to the template
    context = {
        'teacher_count': teacher_count,
        'program_count': program_count,
        'course_count': course_count,
        'student_count': student_count,
    }
    return render(request, 'main_app/admin_dashboard.html', context)

def add_teacher(request):
    if request.method == "POST":
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')  # Redirect to a teacher list page (you can change this)
    else:
        form = TeacherForm()
    
    return render(request, 'main_app/add_teacher.html', {'form': form})

def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'main_app/teacher_list.html', {'teachers': teachers})

def edit_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == "POST":
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherForm(instance=teacher)
    return render(request, 'main_app/add_teacher.html', {'form': form})

def delete_teacher(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    teacher.delete()
    return redirect('teacher_list')


#def manage_student_approval(request):
    students = StudentApproval.objects.select_related('course').all()  # Load course data with students

    if request.method == 'POST':
        action = request.POST.get('action')
        if action:
            action_type, student_id = action.split('_')
            student = StudentApproval.objects.get(id=student_id)

            if action_type == 'approve':
                student.status = 'approved'
                student.save()
                messages.success(request, f"{student.user.username} for {student.course.course_name} has been approved.")
            elif action_type == 'reject':
                student.status = 'rejected'
                student.save()
                messages.warning(request, f"{student.user.username} for {student.course.course_name} has been rejected.")

        return redirect('manage_student_approval')

    return render(request, 'main_app/student_approval.html', {'students': students})
#def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            # Check if a teacher with the given name and email exists
            try:
                teacher = Teacher.objects.get(name=name, email=email)
                # Successful login, redirect to the assignments page or dashboard
                return redirect('teacher_dashboard')  # Replace with actual URL name for teacher dashboard
            except Teacher.DoesNotExist:
                messages.error(request, 'Teacher not found with this name and email.')

    else:
        form = TeacherLoginForm()

    return render(request, 'main_app/teacher_login.html', {'form': form})
def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLoginForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            try:
                teacher = Teacher.objects.get(name=name, email=email)
                request.session['teacher_id'] = teacher.id  # Store teacher ID in session
                return redirect('teacher_dashboard')
            except Teacher.DoesNotExist:
                messages.error(request, 'Teacher not found with this name and email.')
    else:
        form = TeacherLoginForm()

    return render(request, 'main_app/teacher_login.html', {'form': form})

#def teacher_dashboard(request):
    return render(request, 'main_app/teacher_dashboard.html')

#def teacher_dashboard(request):
    teacher = Teacher.objects.get(email=request.user.email)  # Fetch the teacher based on the logged-in user's email

    return render(request, 'main_app/teacher_dashboard.html', {
        'teacher': teacher,
    })

def teacher_dashboard(request):
    teacher_id = request.session.get('teacher_id')  # Get teacher ID from session

    if not teacher_id:
        messages.error(request, "Session expired or you are not logged in. Please log in again.")
        return redirect('teacher_login')

    try:
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        messages.error(request, "Teacher not found. Please log in again.")
        request.session.flush()  # Clear session if teacher not found
        return redirect('teacher_login')

    return render(request, 'main_app/teacher_dashboard.html', {
        'teacher': teacher,
    })

#def add_program(request):
    if request.method == "POST":
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('program_list')  # Redirect to a list page after adding
    else:
        form = ProgramForm()

    return render(request, 'main_app/add_program.html', {'form': form})

def add_program(request):
    if request.method == "POST":
        program_name = request.POST.get("program_name")
        program_code = request.POST.get("program_code")
        duration = request.POST.get("duration")
        description = request.POST.get("description")

        if program_name and program_code and duration:
            Program.objects.create(
                program_name=program_name,
                program_code=program_code,
                duration=duration,
                description=description
            )
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    
    return render(request, "main_app/add_program.html")

#def delete_program(request, program_id):
    if request.method == "POST":
        program = get_object_or_404(Program, id=program_id)
        program.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})


def delete_program(request, program_id):
    if request.method == "POST":
        program = get_object_or_404(Program, id=program_id)
        program.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

def update_program(request, program_id):
    program = get_object_or_404(Program, id=program_id)

    if request.method == "POST":
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            messages.success(request, "Program updated successfully!")
            return redirect("program_list")
    else:
        form = ProgramForm(instance=program)

    return render(request, "main_app/update_program.html", {"form": form, "program": program})


def program_list(request):
    programs = Program.objects.all()  # Fetch all programs
    return render(request, 'main_app/program_list.html', {'programs': programs})


def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_courses')
    else:
        form = CourseForm()
    return render(request, 'main_app/add_course.html', {'form': form})

def view_courses(request):
    courses = Course.objects.all()
    return render(request, 'main_app/view_courses.html', {'courses': courses})

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('view_courses')
    else:
        form = CourseForm(instance=course)
    return render(request, 'main_app/add_course.html', {'form': form})

def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    return redirect('view_courses')

#def logout_view(request):
    logout(request)
    return redirect('home') 


#Assignment
#def create_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)  # Handle file upload
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment created successfully!")
            return redirect('teacher_dashboard')  # Redirect to dashboard after successful creation
    else:
        form = AssignmentForm()

    return render(request, "main_app/create_assignment.html", {"form": form})


#def create_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment created successfully!")  # ✅ Success message
            return redirect('create_assignment')  # Redirect back to the form after submission
    else:
        form = AssignmentForm()

    return render(request, "main_app/create_assignment.html", {"form": form})

#def create_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)  # Don't save to DB yet
            
            # Link the logged-in teacher
            try:
                teacher = Teacher.objects.get(email=request.user.email)
                assignment.teacher = teacher  # Set the teacher field
                
                assignment.save()  # Save with the teacher attached
                messages.success(request, "Assignment created successfully!")  
                return redirect('create_assignment')  
            except Teacher.DoesNotExist:
                messages.error(request, "Teacher account not found!")
    else:
        form = AssignmentForm()

    return render(request, "main_app/create_assignment.html", {"form": form})

def create_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            teacher_id = request.session.get('teacher_id')
            if teacher_id:
                teacher = Teacher.objects.get(id=teacher_id)
                assignment = form.save(commit=False)
                assignment.teacher = teacher
                assignment.save()
                messages.success(request, "Assignment created successfully!")
                return redirect('create_assignment')
            else:
                messages.error(request, "Teacher account not found. Please log in.")
                return redirect('teacher_login')
    else:
        form = AssignmentForm()

    return render(request, "main_app/create_assignment.html", {"form": form})

#def scheduled_assignments(request):
    assignments = Assignment.objects.all()  # Fetch all assignments
    return render(request, 'main_app/scheduled_assignments.html', {'assignments': assignments})

from django.shortcuts import render
from .models import Assignment, Teacher

#def scheduled_assignments(request):
    #try:
        # Get the logged-in teacher based on email
        #teacher = Teacher.objects.get(email=request.user.email)  
        
        # Filter assignments for this teacher only
        #assignments = Assignment.objects.filter(teacher=teacher)

    #except Teacher.DoesNotExist:
        # If the logged-in user is not a teacher, return no assignments
        #assignments = []

    #return render(request, 'main_app/scheduled_assignments.html', {'assignments': assignments})

def scheduled_assignments(request):
    teacher_id = request.session.get('teacher_id')
    if teacher_id:
     assignments = Assignment.objects.filter(teacher_id=teacher_id)
    else:
        assignments = []

    return render(request, 'main_app/scheduled_assignments.html', {'assignments': assignments})    


#def teacher_view_submissions(request):
    # Fetch the assignments that belong to the teacher (based on the courses they teach)
    assignments = Assignment.objects.filter(teacher=request.user.teacher)

    # Fetch the submissions related to those assignments
    submissions = AssignmentSubmission.objects.filter(assignment__in=assignments)

    return render(request, 'teacher_view_submissions.html', {'submissions': submissions})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Teacher, Assignment, AssignmentSubmission

def teacher_view_submissions(request):
    # Get the teacher's ID from the session (assuming it's set during login)
    teacher_id = request.session.get('teacher_id')
    if not teacher_id:
        messages.error(request, "Session expired. Please log in again.")
        return redirect('teacher_login')

    try:
        # Fetch the teacher using the session ID
        teacher = Teacher.objects.get(id=teacher_id)
    except Teacher.DoesNotExist:
        return render(request, 'main_app/teacher_view_submissions.html', {'error': 'Teacher account not found'})

    # Fetch the submissions for the teacher's assignments
    submissions = AssignmentSubmission.objects.filter(
        assignment__teacher=teacher
    ).select_related('student', 'assignment')

    # Render the submissions in the template
    return render(request, 'main_app/teacher_view_submissions.html', {
        'submissions': submissions,
        'teacher': teacher,
    })

#def add_remark(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)

    if request.method == "POST":
        form = AssignmentRemarkForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Remark added successfully!")
            return redirect('teacher_view_submissions')
    else:
        form = AssignmentRemarkForm(instance=submission)

    return render(request, 'main_app/add_remark.html', {
        'form': form,
        'submission': submission,
    })

#def add_remark(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)

    if request.method == "POST":
        form = AssignmentRemarkForm(request.POST, instance=submission)
        if form.is_valid():
            submission.gained_marks = form.cleaned_data['marks_obtained']
            submission.max_marks = form.cleaned_data['max_marks']
            submission.grade = form.cleaned_data['grade']
            submission.comments = form.cleaned_data['comments']
            submission.save()
            
            messages.success(request, "Remark added successfully!")
            return redirect('teacher_view_submissions')
    else:
        form = AssignmentRemarkForm(instance=submission)

    return render(request, 'main_app/add_remark.html', {
        'form': form,
        'submission': submission,
    })
def add_remark(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)

    if request.method == "POST":
        form = AssignmentRemarkForm(request.POST, instance=submission)
        if form.is_valid():
            form.save()
            messages.success(request, "Remark added successfully!")
            return redirect('teacher_view_submissions')
    else:
        form = AssignmentRemarkForm(instance=submission)

    return render(request, 'main_app/add_remark.html', {
        'form': form,
        'submission': submission,
    })





#def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form, creating the User and Student objects
            messages.success(request, "Registration successful.")
            return redirect('home')  # Redirect to login page after registration
    else:
        form = StudentRegistrationForm()

    return render(request, 'main_app/student_register.html', {'form': form})

#def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()  # Save the form and get the student object
            StudentApproval.objects.create(student=student)  # Create approval entry
            messages.success(request, "Registration successful. Awaiting admin approval.")
            return redirect('home')  # Redirect to home page after registration
    else:
        form = StudentRegistrationForm()

    return render(request, 'main_app/student_register.html', {'form': form})

def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()  # Save the form and get the student object
            StudentApproval.objects.create(student=student)  # Create approval entry

            # Store additional details in session
            request.session["address"] = form.cleaned_data["address"]
            request.session["phone_number"] = form.cleaned_data["phone_number"]
            request.session["guardian_name"] = form.cleaned_data["guardian_name"]

            messages.success(request, "Registration successful. Awaiting admin approval.")
            return redirect('home')  # Redirect to home page after registration
    else:
        form = StudentRegistrationForm()

    return render(request, 'main_app/student_register.html', {'form': form})


#def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('student_dashboard')  # Redirect to a dashboard or home page
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = StudentLoginForm()

    return render(request, 'main_app/student_login.html', {'form': form})

#def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                # Check if the student is approved
                if StudentApproval.objects.filter(student=user, is_approved=True).exists():
                    login(request, user)
                    return redirect('student_dashboard')  # Redirect to the dashboard
                else:
                    messages.error(request, 'Your account has not been approved by the admin.')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = StudentLoginForm()

    return render(request, 'main_app/student_login.html', {'form': form})
def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                try:
                    # Fetch the Student instance
                    student = Student.objects.get(user=user)

                    # Check if the student is approved
                    if StudentApproval.objects.filter(student=student, is_approved=True).exists():
                        login(request, user)
                        return redirect('student_dashboard')  # Redirect to the dashboard
                    else:
                        messages.error(request, 'Your account has not been approved by the admin.')
                except Student.DoesNotExist:
                    messages.error(request, 'Student account not found.')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid form data')
    else:
        form = StudentLoginForm()

    return render(request, 'main_app/student_login.html', {'form': form})

#def student_dashboard(request):
    return render(request, 'main_app/student_dashboard.html')  # Create the student_dashboard.html template

#def student_dashboard(request):
    student = request.user.student  # Assuming the user is authenticated and the student is linked to the User model

    # Fetch assignments due for the student's course (pending assignments)
    reminders = Assignment.objects.filter(course=student.course, due_date__gte=datetime.today())

    # Render the dashboard
    return render(request, 'main_app/student_dashboard.html', {
        'student': student,
        'reminders': reminders,
        'course_id': Course.id,
    })
from django.shortcuts import render
from .models import Assignment, AssignmentSubmission

def student_dashboard(request):
    student = request.user.student  # Assuming the logged-in user is a student

    # Get all assignments for the student's course
    course = student.course
    all_assignments = Assignment.objects.filter(course=course)

    # Get assignments that the student has already submitted
    submitted_assignments = AssignmentSubmission.objects.filter(student=student).values_list('assignment_id', flat=True)

    # Filter pending assignments (those not submitted)
    pending_assignments = all_assignments.exclude(id__in=submitted_assignments)

    context = {
        'student': student,
        'reminders': pending_assignments,  # Only show assignments not yet submitted
    }
    return render(request, 'main_app/student_dashboard.html', context)


#def view_assignments(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)
    student = Student.objects.get(user=request.user)

    # Check if the student has already submitted the assignment
    submission = AssignmentSubmission.objects.filter(student=student, assignment=assignment).first()

    if request.method == 'POST' and not submission:
        form = AssignmentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the student submission
            form.instance.student = student
            form.instance.assignment = assignment
            form.save()
            return redirect('student_dashboard')  # Redirect to the student dashboard after submission
    else:
        form = AssignmentUploadForm()

    return render(request, 'view_assignment.html', {
        'assignment': assignment,
        'submission': submission,
        'form': form
    })
##def assignment_list(request, course_id):
    # Fetch assignments for the course (if required, filter by course)
    assignments = Assignment.objects.filter(course_id=course_id)
    return render(request, 'main_app/assignment_list.html', {'assignments': assignments})

def assignment_list(request, course_id):
    assignments = Assignment.objects.filter(course_id=course_id)

    # Get the logged-in student
    student = Student.objects.get(user=request.user)

    # Get the IDs of assignments submitted by this student
    submitted_assignments = AssignmentSubmission.objects.filter(student=student).values_list('assignment_id', flat=True)

    return render(request, 'main_app/assignment_list.html', {
        'assignments': assignments,
        'submitted_assignment_ids': list(submitted_assignments)
    })


def assignment_detail(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    print(f"Assignment ID: {assignment_id}")  # Debugging statement
    print(f"Assignment Title: {assignment.title}")  # Debugging statement
    
    if request.method == 'POST':
        form = AssignmentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_assignment = form.save(commit=False)
            uploaded_assignment.student = request.user  # Assuming User model
            uploaded_assignment.assignment = assignment
            uploaded_assignment.save()
            return redirect('assignment_list', course_id=assignment.course.id)  # Redirect to list after upload
    else:
        form = AssignmentUploadForm()

    return render(request, 'main_app/assignment_detail.html', {
        'assignment': assignment,
        'form': form
    })

#def upload_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        form = AssignmentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_assignment = form.save(commit=False)
            uploaded_assignment.student = student
            uploaded_assignment.assignment = assignment
            uploaded_assignment.save()
            
            messages.success(request, "Assignment uploaded successfully!")  # ✅ Add success message
            
            return redirect('assignment_detail', assignment_id=assignment.id)

    return redirect('assignment_detail', assignment_id=assignment.id)

#def upload_assignment(request, assignment_id):
    if request.method == "POST" and request.FILES.get("file"):
        assignment = Assignment.objects.get(id=assignment_id)
        student = request.user.student  # Get logged-in student
        file = request.FILES["file"]

        # Save the uploaded file in AssignmentSubmission
        AssignmentSubmission.objects.create(student=student, assignment=assignment, file=file)

        messages.success(request, "Assignment uploaded successfully!")

    return redirect('student_dashboard') 


###def upload_assignment(request, assignment_id):
    if request.method == "POST" and request.FILES.get("file"):
        assignment = Assignment.objects.get(id=assignment_id)
        student = request.user.student  # Get logged-in student
        file = request.FILES["file"]

        # Save the uploaded file in AssignmentSubmission
        AssignmentSubmission.objects.create(
            student=student, 
            assignment=assignment, 
            file=file, 
            submitted_at=now()  # Explicitly set submission timestamp
        )

        messages.success(request, "Assignment uploaded successfully!")

    return redirect('student_dashboard')

#def upload_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student

    # Get the existing submission
    submission = AssignmentSubmission.objects.filter(assignment=assignment, student=student).first()

    if request.method == "POST" and request.FILES.get("file"):
        if submission:
            messages.error(request, "❌ You have already submitted this assignment.")
        else:
            submission = AssignmentSubmission.objects.create(
                student=student, 
                assignment=assignment, 
                file=request.FILES["file"], 
                submitted_at=now()
            )
            messages.success(request, "✅ Assignment uploaded successfully!")

    # Ensure submission is passed to the template
    return render(request, "main_app/assignment_detail.html", {
        "assignment": assignment, 
        "submission": submission  # Pass submission to template
    })

def upload_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student

    # Get the existing submission
    submission = AssignmentSubmission.objects.filter(assignment=assignment, student=student).first()

    if request.method == "POST" and request.FILES.get("file"):
        if submission:
            messages.error(request, "❌ You have already submitted this assignment.")
        else:
            submission = AssignmentSubmission.objects.create(
                student=student, 
                assignment=assignment, 
                file=request.FILES["file"], 
                submitted_at=now()
            )
            messages.success(request, "✅ Assignment uploaded successfully!")

            # ✅ Fetch the newly created submission
            submission = AssignmentSubmission.objects.get(assignment=assignment, student=student)

    return render(request, "main_app/assignment_detail.html", {
        "assignment": assignment, 
        "submission": submission  # ✅ Ensure submission is passed to the template
    })



#def upload_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = request.user.student

    # Check if a submission already exists
    submission = AssignmentSubmission.objects.filter(assignment=assignment, student=student).first()
    
    today_date = localdate()

    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]

        if submission:
            messages.error(request, "❌ You have already submitted this assignment.")
        else:
            AssignmentSubmission.objects.create(
                student=student, 
                assignment=assignment, 
                file=file, 
                submitted_at=now()
            )
            messages.success(request, "✅ Assignment uploaded successfully!")
        return redirect('student_dashboard')

    return render(request, "main_app/upload_asignments.html", {
        "assignment": assignment, 
        "submission": submission,  # Pass submission to template
        "today_date": today_date
    })

#def delete_submission(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)

    # Ensure that only the student who uploaded the file can delete it
    if submission.student == request.user.student:
        submission.delete()
        messages.success(request, "✅ Your submission has been deleted.")
    else:
        messages.error(request, "❌ You are not allowed to delete this submission.")

    return redirect('student_dasboard ', assignment_id=submission.assignment.id)
#def delete_submission(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id)

    if request.method == "POST":
        submission.delete()
        messages.success(request, "Submission deleted successfully!")

    return redirect("student_dashboard")
def delete_submission(request, submission_id):
    submission = get_object_or_404(AssignmentSubmission, id=submission_id, student=request.user.student)

    if request.method == "POST":
        submission.delete()
        messages.success(request, "Submission deleted successfully!")

    return redirect("student_dashboard")


#def upload_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    today_date = now().date()  # Get today's date

    # Prevent submission if the due date has passed
    if today_date > assignment.due_date:
        messages.error(request, "❌ The due date has passed. You can no longer submit this assignment.")
        return redirect('student_dashboard')

    if request.method == "POST" and request.FILES.get("file"):
        student = request.user.student  # Get logged-in student
        file = request.FILES["file"]

        # Save the uploaded file in AssignmentSubmission
        AssignmentSubmission.objects.create(
            student=student, 
            assignment=assignment, 
            file=file, 
            submitted_at=now()  # Store the submission timestamp
        )

        messages.success(request, "✅ Assignment uploaded successfully!")
        return redirect('student_dashboard')

    return render(request, "main_app/upload_assignment.html", {"assignment": assignment, "today_date": today_date})



#def upload_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    today_date = localdate()  # Use local date instead of UTC

    # Fix: Allow submissions ON the due date
    if today_date > assignment.due_date:
        messages.error(request, "❌ The due date has passed. You can no longer submit this assignment.")
        return redirect('student_dashboard')

    if request.method == "POST" and request.FILES.get("file"):
        student = request.user.student  # Get logged-in student
        file = request.FILES["file"]

        # Save the uploaded file in AssignmentSubmission
        AssignmentSubmission.objects.create(
            student=student, 
            assignment=assignment, 
            file=file, 
            submitted_at=now()
        )

        messages.success(request, "✅ Assignment uploaded successfully!")
        return redirect('student_dashboard')

    return render(request, "main_app/upload_assignment.html", {
        "assignment": assignment, 
        "today_date": today_date
    })


#def upload_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    today_date = localdate()  # Get local date (fixing UTC mismatch)

    # Allow submissions ON the due date
    if today_date > assignment.due_date:
        messages.error(request, "❌ The due date has passed. You can no longer submit this assignment.")
        return redirect('student_dashboard')

    if request.method == "POST" and request.FILES.get("file"):
        student = request.user.student  # Get logged-in student
        file = request.FILES["file"]

        # Save the uploaded file in AssignmentSubmission
        AssignmentSubmission.objects.create(
            student=student, 
            assignment=assignment, 
            file=file, 
            submitted_at=now()
        )

        messages.success(request, "✅ Assignment uploaded successfully!")
        return redirect('student_dashboard')

    return render(request, "main_app/upload_assignment.html", {
        "assignment": assignment, 
        "today_date": today_date
    })

#def student_view_remarks(request):
    student = request.user.student  # Assuming the user is logged in and has a student profile
    submissions = AssignmentSubmission.objects.filter(student=student).select_related('assignment')

    return render(request, 'main_app/student_view_remarks.html', {'submissions': submissions})

#def student_view_remarks(request):
    student = request.user.student  # Ensure the logged-in student is fetched
    submissions = AssignmentSubmission.objects.filter(student=student).select_related('assignment')

    return render(request, 'main_app/student_view_remarks.html', {'submissions': submissions})
def student_view_remarks(request):
    student = request.user.student  # Fetch the logged-in student
    submissions = AssignmentSubmission.objects.filter(student=student).select_related('assignment')

    return render(request, 'main_app/student_view_remarks.html', {'submissions': submissions})

def student_performance_chart(request):
    submissions = AssignmentSubmission.objects.filter(student=request.user.student)
    labels = []
    data = []
    marks_info = []

    for sub in submissions:
        labels.append(sub.assignment.title)

        if sub.grade:
            marks_info.append(f"Grade: {sub.grade}")

            if sub.grade in ['A', 'B']:
                data.append(3)  # Good
            elif sub.grade == 'C':
                data.append(2)  # Needs Improvement
            elif sub.grade in ['D', 'F']:
                data.append(1)  # Poor
        else:
            data.append(0)  # Not Available
            marks_info.append("Not Available")

    return render(request, 'main_app/student_performance_chart.html', {
        'labels': labels,
        'data': data,
        'marks_info': marks_info,
    })

#def manage_student_approval(request):
    students = StudentApproval.objects.select_related('student').all()

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        action = request.POST.get('action')

        if student_id and action:
            student_approval = get_object_or_404(StudentApproval, id=student_id)

            if action == 'approve':
                student_approval.is_approved = True
                student_approval.save()
                messages.success(request, f"{student_approval.student.username} has been approved.")
            elif action == 'reject':
                student_approval.is_approved = False
                student_approval.save()
                messages.warning(request, f"{student_approval.student.username} has been rejected.")

        return redirect('manage_student_approval')

    return render(request, 'main_app/student_approval.html', {'students': students})


def manage_student_approval(request):
    students = StudentApproval.objects.select_related('student__user').all()

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        action = request.POST.get('action')

        if student_id and action:
            student_approval = get_object_or_404(StudentApproval, id=student_id)

            if action == 'approve':
                student_approval.is_approved = True
                student_approval.save()
                messages.success(request, f"{student_approval.student.user.username} has been approved.")
            elif action == 'reject':
                student_approval.is_approved = False
                student_approval.save()
                messages.warning(request, f"{student_approval.student.user.username} has been rejected.")

        return redirect('manage_student_approval')

    return render(request, 'main_app/student_approval.html', {'students': students})

def student_profile(request):
    student = request.user.student  # Get the logged-in student
    return render(request, 'main_app/student_profile.html', {'student': student})

#def student_profile(request):
    student = get_object_or_404(Student, user=request.user)

    # Temporary data if not in model (stored in session or manually entered)
    extra_details = {
        "address": request.session.get("address", "Not Provided"),
        "phone_number": request.session.get("phone_number", "Not Provided"),
        "guardian_name": request.session.get("guardian_name", "Not Provided"),
    }

    return render(request, "main_app/student_profile.html", {"student": student, "extra_details": extra_details})

#def student_profile(request):
    student = request.user.student  # Get the student object from the logged-in user

    # Extra details (if not stored in model, provide a fallback)
    address = getattr(student, 'address', "Not Provided")
    phone_number = getattr(student, 'phone_number', "Not Provided")
    guardian_name = getattr(student, 'guardian_name', "Not Provided")

    return render(request, "main_app/student_profile.html", {
        "student": student,
        "address": address,
        "phone_number": phone_number,
        "guardian_name": guardian_name
    })

#def student_profile(request):
    student = get_object_or_404(Student, user=request.user)

    return render(request, "main_app/student_profile.html", context)



def update_profile(request):
    student = request.user.student

    if request.method == 'POST':
        form = StudentUpdateForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('student_profile')
    else:
        form = StudentUpdateForm(instance=student)

    return render(request, 'main_app/update_profile.html', {'form': form})

def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # ✅ Directly delete without checking if the user is a teacher
    assignment.delete()
    messages.success(request, "Assignment deleted successfully!")

    return redirect('scheduled_assignments')

#def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully!")
            return redirect('scheduled_assignments')  # Redirect to the assignments list
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'main_app/edit_assignment.html', {'form': form, 'assignment': assignment})
#def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully!")
            return redirect('scheduled_assignments')  # Make sure this URL name is correct
        else:
            print("Form errors:", form.errors)  # Debugging line
            messages.error(request, "Failed to update assignment. Please check the errors.")

    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'main_app/edit_assignment.html', {'form': form, 'assignment': assignment})

#def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully!")
            return redirect('scheduled_assignments')  # Redirect after successful update
        else:
            print(form.errors)  # Print errors to the console for debugging
            messages.error(request, "Failed to update assignment. Please check the form and try again.")
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'main_app/edit_assignment.html', {'form': form, 'assignment': assignment})

#def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assignment updated successfully!")
            return redirect('scheduled_assignments')  
        else:
            print(form.errors)  # Debugging: Print errors in the console
            messages.error(request, "Failed to update the assignment. Please check your inputs.")
    else:
        form = AssignmentForm(instance=assignment)

    return render(request, 'main_app/edit_assignment.html', {'form': form, 'assignment': assignment})

def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    if request.method == 'POST':
        form = EditAssignmentForm(request.POST, request.FILES, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Assignment updated successfully!")
            return redirect('scheduled_assignments')
        else:
            print("Form Errors:", form.errors)  # Debugging
            messages.error(request, "❌ Failed to update the assignment. Please check your inputs.")

    else:
        form = EditAssignmentForm(instance=assignment)

    return render(request, 'main_app/edit_assignment.html', {'form': form, 'assignment': assignment})


#def teacher_students(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    students = Student.objects.filter(course__in=teacher.courses_assigned.all())

    return render(request, 'main_app/teacher_students.html', {'students': students})

#def teacher_students(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    # Fetch students who are enrolled in the teacher's assigned courses
    students = Student.objects.filter(course__in=teacher.courses_assigned.all()).select_related("course", "user")

    query = request.GET.get("q")
    selected_student = None
    assignments = None
    submissions = None

    if query:
        selected_student = students.filter(name__icontains=query).first()
        if selected_student:
            assignments = Assignment.objects.filter(course=selected_student.course)
            submissions = AssignmentSubmission.objects.filter(student=selected_student)

    return render(request, "main_app/teacher_students.html", {
        "students": students,
        "selected_student": selected_student,
        "assignments": assignments,
        "submissions": submissions,
        "query": query,
    })

def teacher_students(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)

    # Get all students in the teacher's assigned courses
    students = Student.objects.filter(course__in=teacher.courses_assigned.all()).select_related("course", "user")

    query = request.GET.get("q")  # Search input
    selected_student = None
    submissions = None

    if query:
        selected_student = students.filter(name__icontains=query).first()
        if selected_student:
            # Fetch only the assignments that the student has submitted
            submissions = AssignmentSubmission.objects.filter(student=selected_student).select_related("assignment", "assignment__course")

    return render(request, "main_app/teacher_students.html", {
        "students": students,
        "selected_student": selected_student,
        "submissions": submissions,
        "query": query,

    })    