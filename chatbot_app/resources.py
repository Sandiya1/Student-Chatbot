# chatbot_app/resources.py
from import_export import resources
from .models import StudentProfile

class StudentProfileResource(resources.ModelResource):
    class Meta:
        model = StudentProfile
        fields = '__all__'
        from import_export import resources
from .models import Subject

class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        fields = '__all__'

from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget
from .models import ExamMark, Attendance, StudentProfile, Subject

class CombinedMarkAttendanceResource(resources.ModelResource):
    student = fields.Field(
        column_name='student_username',
        attribute='student',
        widget=ForeignKeyWidget(StudentProfile, 'user__username')
    )
    subject = fields.Field(
        column_name='subject_name',
        attribute='subject',
        widget=ForeignKeyWidget(Subject, 'name')
    )
    exam_type = fields.Field(column_name='exam_type')
    marks = fields.Field(column_name='marks')
    attended_classes = fields.Field(column_name='attended_classes')
    total_classes = fields.Field(column_name='total_classes')

    class Meta:
        model = ExamMark
        fields = ('student', 'subject', 'exam_type', 'marks', 'attended_classes', 'total_classes')
from import_export import resources
from .models import Subject

class SubjectResource(resources.ModelResource):
    class Meta:
        model = Subject
        fields = ('id', 'name')  # or just '__all__'
