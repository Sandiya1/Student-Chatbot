# models.py

from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    student_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    total_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    pending_fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.user.username

class ExamMark(models.Model):
    EXAM_CHOICES = [
        ('CAT1', 'CAT1'),
        ('CAT2', 'CAT2'),
        ('CAT3', 'CAT3'),
        ('MODEL', 'Model Exam'),

    ]
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=20, choices=EXAM_CHOICES)
    marks = models.IntegerField()

    def __str__(self):
        return f'{self.student.user.username} - {self.subject.name} - {self.exam_type}'
class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    total_classes = models.IntegerField(default=0)
    attended_classes = models.IntegerField(default=0)

    def percentage(self):
        return (self.attended_classes / self.total_classes * 100) if self.total_classes > 0 else 0

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.name}"
