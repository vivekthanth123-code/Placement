from django.shortcuts import render, redirect,  get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib.auth.models import User
from .models import StudentProfile
from .forms import RegisterForm, ProfileForm, ResumeForm
from .models import StudentProfile, Question, Choice, StudyMaterial, JobPost, JobApplication, Resume
from .models import  StudentProfile, Resume
from django.contrib.admin.views.decorators import staff_member_required
from .models import QuizQuestion, QuizOption, QuizAttempt, UserAnswer
from django.db.models import F
from .models import Category, QuizQuestion
from .models import MaterialCategory, MaterialDownload
from django.http import FileResponse

# ================= HOME =================
def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')

# ================= REGISTER =================
@transaction.atomic
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            StudentProfile.objects.create(
                user=user,
                phone=profile_form.cleaned_data.get('phone', ''),
                college=profile_form.cleaned_data.get('college', ''),
                branch=profile_form.cleaned_data.get('branch', ''),
                graduation_year=profile_form.cleaned_data.get('graduation_year', None),
                experience=profile_form.cleaned_data.get('experience', ''),
                extra_info=profile_form.cleaned_data.get('extra_info', ''),
                profile_image=profile_form.cleaned_data.get('profile_image', 'profile_images/default.png')
            )
            login(request, user)
            messages.success(request, "Account created and logged in successfully!")
            return redirect('student_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = RegisterForm()
        profile_form = ProfileForm()

    return render(request, 'register.html', {
        'form': form,
        'profile_form': profile_form
    })

# ================= LOGIN =================
def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect('student_dashboard')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('login')

def forgot_password(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password and confirm_password:
            if new_password == confirm_password:
                # For demo purposes, we'll just show a success message
                # In a real app, you'd need to identify the user somehow
                messages.success(request, "Password reset successfully! (Demo - no actual user updated)")
                return redirect('login')
            else:
                messages.error(request, "Passwords do not match")
        else:
            messages.error(request, "Please fill in all fields")
    
    return render(request, 'forgot_password.html')

# ================= STUDENT DASHBOARD =================
@login_required
def student_dashboard(request):
    profile, created = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "photo":
            image = request.FILES.get("profile_image")
            if image:
                profile.profile_image = image
                profile.save()

        elif form_type == "profile":
            profile.phone = request.POST.get("phone", "")
            profile.branch = request.POST.get("branch", "")
            profile.expected_salary = request.POST.get("expected_salary") or None
            profile.technology = request.POST.get("technology", "")
            profile.experience = request.POST.get("experience", "")
            profile.save()

    resume = Resume.objects.filter(user=request.user).first()
    applied_jobs = JobApplication.objects.filter(
        user=request.user
    ).select_related('job').order_by('-applied_at')

    return render(request, "student_dashboard.html", {
        "profile": profile,
        "resume": resume,
        "applied_jobs": applied_jobs,
    })

# ================= QUIZ HOME =================
@login_required
def quiz_home(request):
    categories = Category.objects.all()
    return render(request, 'quiz_home.html', {'categories': categories})

# ================= CATEGORY QUIZ =================
@login_required
def category_quiz(request, slug):
    category = get_object_or_404(Category, slug=slug)
    questions = category.questions.prefetch_related('options').all()

    if request.method == "POST":
        score = 0
        total_questions = questions.count()

        # Create quiz attempt
        attempt = QuizAttempt.objects.create(
            user=request.user,
            category=category,
            score=0,
            total_questions=total_questions
        )

        # Save each answer
        for question in questions:
            selected_option_id = request.POST.get(str(question.id))
            
            if selected_option_id:
                try:
                    selected_option = QuizOption.objects.get(id=int(selected_option_id))
                    
                    # Save user answer
                    UserAnswer.objects.create(
                        attempt=attempt,
                        question=question,
                        selected_option=selected_option
                    )
                    
                    # Check if correct
                    if selected_option.is_correct:
                        score += 1
                except QuizOption.DoesNotExist:
                    pass

        # Update attempt score
        attempt.score = score
        attempt.save()

        return redirect('result', attempt_id=attempt.id)

    return render(request, 'category_quiz.html', {
        'category': category,
        'questions': questions
    })

# ================= QUIZ RESULT =================
@login_required
def result(request, attempt_id):
    attempt = QuizAttempt.objects.get(id=attempt_id, user=request.user)
    user_answers = UserAnswer.objects.filter(attempt=attempt).select_related('question', 'selected_option')

    answers = []
    for ua in user_answers:
        correct_option = ua.question.options.filter(is_correct=True).first()
        answers.append({
            'question': ua.question,
            'selected_option': ua.selected_option,
            'is_correct': ua.selected_option.is_correct,
            'correct_option': correct_option
        })

    passed = attempt.score >= attempt.total_questions * 0.7  # Assuming 70% pass

    context = {
        "attempt": attempt,
        "answers": answers,
        "passed": passed
    }

    return render(request, "result.html", context)

# ================= UPLOAD RESUME =================
@login_required
def upload_resume(request):
    if request.method == "POST" and request.FILES.get("resume"):
        file = request.FILES["resume"]
        resume_obj, _ = Resume.objects.get_or_create(user=request.user)
        resume_obj.resume_file = file
        resume_obj.save()
        messages.success(request, "Resume uploaded successfully.")
        return redirect("profile")
    return render(request, "upload_resume.html")

# ================= PROFILE =================
@login_required
def profile(request):
    profile = StudentProfile.objects.filter(user=request.user).first()
    resume = Resume.objects.filter(user=request.user).first()
    return render(request, "profile.html", {
        "profile": profile,
        "resume": resume
    })

# ================= STUDY MATERIAL =================
def material_categories(request):
    categories = MaterialCategory.objects.all()
    return render(request, 'study_materials.html', {
        'categories': categories
    })

def material_list(request, category_id):
    category = get_object_or_404(MaterialCategory, id=category_id)
    materials = StudyMaterial.objects.filter(category=category)
    return render(request, 'material_list.html', {
        'category': category,
        'materials': materials
    })

def download_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)

    if request.user.is_authenticated:
        MaterialDownload.objects.create(
            user=request.user,
            material=material
        )

    return FileResponse(material.pdf.open(), as_attachment=True)

# ================= STUDENT MANAGEMENT =================
@staff_member_required
def student_list(request):
    students = StudentProfile.objects.select_related('user').all()
    return render(request, 'student_list.html', {
        'students': students
    })

@staff_member_required
def student_delete(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)
    student.delete()
    return redirect("student_list")

@staff_member_required
def student_update(request, pk):
    student = get_object_or_404(StudentProfile, pk=pk)

    if request.method == "POST":
        student.phone = request.POST.get("phone")
        student.branch = request.POST.get("branch")
        student.technology = request.POST.get("technology")
        student.user.email = request.POST.get("email")
        student.user.username = request.POST.get("username")
        student.user.save()
        student.save()
        return redirect("student_list")

    return render(request, "student_update.html", {"student": student})

# ================= JOBS =================
@login_required
def jobs(request):
    category = request.GET.get('category')
    jobs_list = JobPost.objects.all()

    if category:
        jobs_list = jobs_list.filter(category=category)

    return render(request, 'jobs.html', {
        'jobs': jobs_list,
        'selected_category': category
    })

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)
    already_applied = JobApplication.objects.filter(
        user=request.user,
        job=job
    ).exists()

    return render(request, 'job_detail.html', {
        'job': job,
        'already_applied': already_applied
    })

@login_required
def apply_job(request, job_id):
    job = get_object_or_404(JobPost, id=job_id)

    if not JobApplication.objects.filter(user=request.user, job=job).exists():
        JobApplication.objects.create(user=request.user, job=job)

    return redirect('job_detail', job_id=job.id)


def forgot_password(request):
    if request.method == 'POST':
        username        = request.POST.get('username', '').strip()
        new_password    = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')

        # 1. Check username exists
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'No account found with that username.')
            return render(request, 'forgot_password.html')

        # 2. Check passwords match
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'forgot_password.html')

        # 3. Check password length (basic validation)
        if len(new_password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
            return render(request, 'forgot_password.html')

        # 4. Set the new password
        user.set_password(new_password)
        user.save()

        messages.success(request, 'Password reset successfully! You can now log in.')
        return redirect('login')

    return render(request, 'forgot_password.html')