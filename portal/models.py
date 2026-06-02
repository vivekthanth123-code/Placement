from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

# ================= CATEGORY =================
class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


# ================= STUDENT PROFILE =================
class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField(max_length=15, blank=True)
    college = models.CharField(max_length=200, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    experience = models.CharField(max_length=200, blank=True)
    expected_salary = models.IntegerField(null=True, blank=True)
    technology = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(upload_to="profile_images/", default="profile_images/default.png", blank=True)
    extra_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


# ================= QUESTION & CHOICE =================
class Question(models.Model):
    question_text = models.TextField()
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.question_text[:50]


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.choice_text} ({'Correct' if self.is_correct else 'Wrong'})"


# ================= QUIZ =================
class QuizQuestion(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='questions'  # <-- add this
    )
    question_text = models.TextField()

# -----------------------------------

class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="options")
    option_text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option_text

    # -------------------------


# -------------------------

class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    score = models.IntegerField()
    total_questions = models.IntegerField()
    attempt_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.category.name} ({self.score}/{self.total_questions})"

# ------------------------------------------

class QuizResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    total_questions = models.IntegerField()
    percentage = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.total_questions > 0:
            self.percentage = (self.score / self.total_questions) * 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - {self.score}/{self.total_questions}"


# ================= RESUME, STUDY MATERIAL & JOB POST =================
class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="resume")
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

# --------------------------------------------------------
# ----------------------------------------------

# CATEGORY (Frontend / Backend)
class MaterialCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# STUDY MATERIAL
class StudyMaterial(models.Model):
    category = models.ForeignKey(MaterialCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    pdf = models.FileField(upload_to='materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# DOWNLOAD TRACKING (IMPORTANT 🔥)
class MaterialDownload(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(StudyMaterial, on_delete=models.CASCADE)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.material.title}"

# ------------------------------------------------
# --------------------------------------------------

class JobPost(models.Model):
    JOB_TYPE_CHOICES = (
        ('frontend', 'Frontend'),
        ('backend', 'Backend'),
        ('fullstack', 'Full Stack'),
    )

    company_name = models.CharField(max_length=200)
    job_role = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    location = models.CharField(max_length=100, blank=True)
    salary = models.CharField(max_length=100, blank=True)
    company_image = models.ImageField(upload_to='company/', blank=True, null=True)

    # ⭐ ADD THESE NEW FIELDS
    description = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    skills_required = models.CharField(max_length=300, blank=True)
    experience = models.CharField(max_length=100, blank=True)

    last_date = models.DateField()
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-posted_at']

    def __str__(self):
        return f"{self.company_name} - {self.job_role}"

# -------apply job ---------

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} applied for {self.job.job_role}"

        # ------------------------------------------

class UserAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOption, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.attempt.user.username} - {self.question.question_text[:30]}"