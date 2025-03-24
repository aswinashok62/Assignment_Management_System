from django import forms
from django.core.validators import RegexValidator
from .models import Teacher, Course, Program,Assignment,Student,AssignmentSubmission
from django.forms.widgets import DateInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from datetime import date
from django.core.exceptions import ValidationError


class TeacherLoginForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()


class TeacherForm(forms.ModelForm):
    phone = forms.CharField(
        max_length=10,
        validators=[RegexValidator(r'^\d{10}$', message="Phone number must be exactly 10 digits.")]
    )
    date_of_joining = forms.DateField(
        widget=DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Teacher
        fields = ['name', 'employee_id', 'email', 'phone',  'courses_assigned', 'qualification', 'date_of_joining']

class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['program_name', 'program_code', 'duration', 'description']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_name', 'course_code', 'program', 'credits', 'semester', 'description']
        widgets = {
            'course_name': forms.TextInput(attrs={'class': 'form-control'}),
            'course_code': forms.TextInput(attrs={'class': 'form-control'}),
            'program': forms.Select(attrs={'class': 'form-control'}),
            'credits': forms.NumberInput(attrs={'class': 'form-control'}),
            'semester': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

#class AssignmentForm(forms.ModelForm):
    #file = forms.FileField(
        #required=False,  # Make file optional
        #widget=forms.ClearableFileInput(attrs={'accept': '.pdf'})  # Restrict file upload type
    #)

    #class Meta:
       # model = Assignment
        #fields = ['program', 'course',  'title', 'description', 'due_date', 'file']

        #widgets = {
            #'due_date': forms.DateInput(attrs={'type': 'date'}),
        #}        

class AssignmentForm(forms.ModelForm):
    file = forms.FileField(
        required=False,  # Make file optional
        widget=forms.ClearableFileInput(attrs={'accept': '.pdf'})  # Restrict file upload type
    )

    class Meta:
        model = Assignment
        fields = ['program', 'course', 'title', 'description', 'due_date', 'file']

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < date.today():
            raise ValidationError("Due date cannot be in the past. Please select today or a future date.")
        return due_date        

#class StudentRegistrationForm(forms.ModelForm):
    # Fields for username, email, and password (User model)
    #username = forms.CharField(max_length=100)
    #email = forms.EmailField()
    #password = forms.CharField(widget=forms.PasswordInput)
    #password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    
    # Fields for Student details
    #program = forms.ModelChoiceField(queryset=Program.objects.all())
    #course = forms.ModelChoiceField(queryset=Course.objects.all())
    
    #class Meta:
        model = Student
        fields = ['name', 'program', 'course']  # Student-specific fields

    #def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        
        # Check if passwords match
        if password != password2:
            raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data

    #def save(self, commit=True):
        # First, create the User object
        user = User.objects.create_user(username=self.cleaned_data["username"], 
                                        password=self.cleaned_data["password"], 
                                        email=self.cleaned_data["email"])

        # Now create the Student object and link to the created User
        student = super().save(commit=False)
        student.user = user  # Link the Student to the User

        if commit:
            student.save()

        return student
    

class StudentRegistrationForm(forms.ModelForm):
    # Fields for username, email, and password (User model)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    # Fields for Student details
    program = forms.ModelChoiceField(queryset=Program.objects.all())
    course = forms.ModelChoiceField(queryset=Course.objects.all())

    # New Fields
    address = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(
        max_length=10, 
        min_length=10, 
        required=True, 
        error_messages={'min_length': "Phone number must be 10 digits.", 'max_length': "Phone number must be 10 digits."}
    )
    guardian_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Student
        fields = ['name', 'program', 'course', 'address', 'phone_number', 'guardian_name']  # Include new fields

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        # Check if passwords match
        if password != password2:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        # First, create the User object
        user = User.objects.create_user(
            username=self.cleaned_data["username"], 
            password=self.cleaned_data["password"], 
            email=self.cleaned_data["email"]
        )

        # Now create the Student object and link to the created User
        student = super().save(commit=False)
        student.user = user  # Link the Student to the User
        student.address = self.cleaned_data["address"]
        student.phone_number = self.cleaned_data["phone_number"]
        student.guardian_name = self.cleaned_data["guardian_name"]

        if commit:
            student.save()

        return student

    

class StudentLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))

class AssignmentUploadForm(forms.ModelForm):
    class Meta:
        model = AssignmentSubmission
        fields = ['file']  # Only file field for upload

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file and not uploaded_file.name.endswith('.pdf'):
            raise forms.ValidationError("Only PDF files are allowed.")
        return uploaded_file

class AssignmentRemarkForm(forms.ModelForm):
    max_marks = forms.IntegerField(label="Maximum Marks")
    gained_marks = forms.IntegerField(label="Marks Obtained")  # Use gained_marks here
    grade = forms.ChoiceField(
        choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('F', 'F')],
        label="Grade"
    )
    comments = forms.CharField(widget=forms.Textarea, required=False, label="Comments")

    class Meta:
        model = AssignmentSubmission
        fields = ['gained_marks', 'max_marks', 'grade', 'comments']


class StudentUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Student
        fields = ['name','program','course']



class EditAssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'due_date', 'file']  # Exclude 'program' and 'course'

        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
        }
