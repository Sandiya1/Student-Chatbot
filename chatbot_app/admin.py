from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import StudentProfile, Subject, ExamMark, Attendance
from .resources import (
    StudentProfileResource,
    SubjectResource,
    CombinedMarkAttendanceResource
)

# ✅ Inline marks under Student
class ExamMarkInline(admin.TabularInline):
    model = ExamMark
    extra = 1

# ✅ Student Profile Admin (import/export enabled)
@admin.register(StudentProfile)
class StudentProfileAdmin(ImportExportModelAdmin):
    resource_class = StudentProfileResource
    inlines = [ExamMarkInline]
    list_display = ('user', 'email', 'total_fees', 'pending_fees')
    search_fields = ('user__username', 'email')
    list_filter = ('total_fees', 'pending_fees')

# ✅ Subject Admin (import/export enabled)
@admin.register(Subject)
class SubjectAdmin(ImportExportModelAdmin):
    resource_class = SubjectResource
    list_display = ('name',)
    search_fields = ('name',)

# ✅ ExamMark Admin (combined with attendance import)
@admin.register(ExamMark)
class ExamMarkAttendanceAdmin(ImportExportModelAdmin):
    resource_class = CombinedMarkAttendanceResource

    def after_import_instance(self, instance, new, row_number=None, **kwargs):
        # Automatically handle attendance update during import
        if row_number:
            attended = row_number.get("attended_classes")
            total = row_number.get("total_classes")
            if attended is not None and total is not None:
                Attendance.objects.update_or_create(
                    student=instance.student,
                    subject=instance.subject,
                    defaults={
                        "attended_classes": attended,
                        "total_classes": total
                    }
                )

# ✅ Attendance Admin (view/edit only, no import)
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'attended_classes', 'total_classes')
    list_filter = ('subject',)
    search_fields = ('student__user__username', 'subject__name')


# ✅ Optional: Custom Admin Site with logout override
from django.contrib.admin import AdminSite
from django.shortcuts import redirect
from django.contrib.auth import logout

class MyAdminSite(AdminSite):
    def logout(self, request, extra_context=None):
        logout(request)
        return redirect('/')  # Your custom login page

resource_class = SubjectResource

