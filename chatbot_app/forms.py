from django import forms
from .models import StudentProfile, Subject, ExamMark
from django.contrib.auth.models import User

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['user', 'student_id', 'dob', 'email', 'total_fees', 'pending_fees']

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name']

class ExamMarkForm(forms.ModelForm):
    class Meta:
        model = ExamMark
        fields = ['student', 'subject', 'exam_type', 'marks']
