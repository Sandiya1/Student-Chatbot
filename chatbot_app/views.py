from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required  # ✅ Correct import
from django.contrib.auth.forms import UserCreationForm
from .models import StudentProfile, Subject, ExamMark
from .forms import StudentProfileForm, SubjectForm, ExamMarkForm

def custom_login(request):
    if request.method == 'POST':
        username = request.POST['username'].strip()
        password = request.POST['password'].strip()

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('/admin/')  # Optional admin redirect
            return redirect('/dashboard/')
        else:
            return render(request, 'registration/login.html', {
                'error': 'Invalid credentials'
            })
    return render(request, 'registration/login.html')


def custom_logout(request):
    logout(request)
    return redirect('login')


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user, student_id=f"ID{user.id}")
            login(request, user)
            return redirect('/update-profile/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


@login_required
def update_profile(request):
    student = StudentProfile.objects.get(user=request.user)
    if request.method == 'POST':
        student.email = request.POST.get('email')
        student.dob = request.POST.get('dob')
        student.save()
        return redirect('/dashboard/')
    return render(request, 'chatbot_app/update_profile.html', {'student': student})


@login_required
def dashboard_view(request):
    student = StudentProfile.objects.get(user=request.user)
    return render(request, 'chatbot_app/dashboard.html', {'student': student})

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from fuzzywuzzy import process
from .models import StudentProfile, Subject, ExamMark, Attendance

@login_required
def chat(request):
    response = None
    profile = get_object_or_404(StudentProfile, user=request.user)

    if request.method == 'POST':
        message = request.POST.get('message', '').lower()

        # Fuzzy match subject
        subjects = Subject.objects.all()
        subject_names = [s.name.lower() for s in subjects]
        matched_subject = None
        matched_subject_obj = None
        if subject_names:
            match = process.extractOne(message, subject_names)
            if match and match[1] >= 70:
                matched_subject = match[0]
                matched_subject_obj = next((s for s in subjects if s.name.lower() == matched_subject), None)

        # Fuzzy match exam type
        exam_types = ["cat1", "cat2", "cat3", "model"]
        exam_type_map = {
            "cat1": "CAT1",
            "cat2": "CAT2",
            "cat3": "CAT3",
            "model": "MODEL",
            
        }
        matched_exam = None
        match = process.extractOne(message, exam_types)
        if match and match[1] >= 70:
            matched_exam = match[0]

        # Get all student data
        marks = ExamMark.objects.filter(student=profile)
        attendances = Attendance.objects.filter(student=profile)

        # 🎯 MARKS SECTION
        if ("mark" in message or "marks" in message or "grade" in message or
            matched_subject_obj or matched_exam):

            if matched_exam and matched_subject_obj:
                mark = ExamMark.objects.filter(
                    student=profile,
                    subject=matched_subject_obj,
                    exam_type=exam_type_map[matched_exam]
                ).first()
                response = (
                    f"{matched_subject_obj.name.title()} - {exam_type_map[matched_exam]}: {mark.marks}"
                    if mark else
                    f"No {exam_type_map[matched_exam]} mark found for {matched_subject_obj.name.title()}."
                )

            elif matched_subject_obj:
                subject_marks = marks.filter(subject=matched_subject_obj)
                if subject_marks.exists():
                    response = "<br>".join([
                        f"{m.exam_type}: {m.marks}" for m in subject_marks
                    ])
                else:
                    response = f"No marks found for {matched_subject_obj.name.title()}."

            elif matched_exam:
                exam_marks = marks.filter(exam_type=exam_type_map[matched_exam])
                if exam_marks.exists():
                    response = "<br>".join([
                        f"{m.subject.name}: {exam_type_map[matched_exam]} = {m.marks}"
                        for m in exam_marks
                    ])
                else:
                    response = f"No marks found for {exam_type_map[matched_exam]}."

            else:
                response = "Please mention the subject or exam like 'maths cat1'."

        # 💸 FEES SECTION
        elif "fee" in message:
            response = f"Total Fees: ₹{profile.total_fees}, Pending Fees: ₹{profile.pending_fees}"

        # 👤 PERSONAL INFO SECTION
        elif "info" in message or "profile" in message or "personal" in message:
            response = (
                f"<strong>Student ID:</strong> {profile.student_id}<br>"
                f"<strong>Name:</strong> {profile.user.get_full_name() or profile.user.username}<br>"
                f"<strong>Email:</strong> {profile.email}<br>"
                f"<strong>DOB:</strong> {profile.dob}<br>"
                f"<strong>Username:</strong> {profile.user.username}"
            )

        # 🕒 ATTENDANCE SECTION
        elif "attendance" in message:
            if attendances.exists():
                response = "<br>".join([
                    f"{a.subject.name}: {a.attended_classes}/{a.total_classes} classes "
                    f"({a.percentage():.2f}%)"
                    for a in attendances
                ])
            else:
                response = "No attendance records available."

        # 🤖 DEFAULT FALLBACK
        else:
            response = "🤖 I didn't understand. Try asking about marks, fees, attendance, or your profile."

    return render(request, 'chatbot_app/chat.html', {'response': response})


@staff_member_required
def admin_data_entry(request):
    student_form = StudentProfileForm()
    subject_form = SubjectForm()
    exam_form = ExamMarkForm()

    if request.method == "POST":
        if "submit_student" in request.POST:
            student_form = StudentProfileForm(request.POST)
            if student_form.is_valid():
                student_form.save()
        elif "submit_subject" in request.POST:
            subject_form = SubjectForm(request.POST)
            if subject_form.is_valid():
                subject_form.save()
        elif "submit_exam" in request.POST:
            exam_form = ExamMarkForm(request.POST)
            if exam_form.is_valid():
                exam_form.save()

    return render(request, 'chatbot_app/admin_entry.html', {
        'student_form': student_form,
        'subject_form': subject_form,
        'exam_form': exam_form,
    })
# Optionally later
def reset_password(request):
    if request.method == 'POST':
        pwd1 = request.POST.get('new_password')
        pwd2 = request.POST.get('confirm_password')
        if pwd1 == pwd2:
            request.user.set_password(pwd1)
            request.user.save()
            return redirect('login')
    return render(request, 'chatbot_app/reset_password.html')
