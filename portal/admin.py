from django.contrib import admin
from .models import (
    Category, QuizQuestion, QuizOption, QuizResult, QuizAttempt,
    StudentProfile, Question, Choice, Resume, JobPost, JobApplication
)
from .models import MaterialCategory, StudyMaterial, MaterialDownload
# ================= CATEGORY =================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

# ================= QUIZ OPTION INLINE =================
class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 4

# ================= QUIZ QUESTION =================
@admin.register(QuizQuestion)
class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ("question_text", "category",)
    inlines = [QuizOptionInline]
    list_filter = ("category",)
    search_fields = ("question_text",)

# ================= QUESTION & CHOICE =================
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 4

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ("question_text", "category", "created_at")
    search_fields = ("question_text", "category")
    list_filter = ("category",)

# ================= QUIZ RESULT =================
@admin.register(QuizResult)
class QuizResultAdmin(admin.ModelAdmin):
    list_display = ("user", "score", "total_questions", "percentage", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)

# ================= QUIZ ATTEMPT =================

# ================= STUDENT PROFILE =================
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "branch", "technology", "expected_salary", "created_at")
    search_fields = ("user__username", "phone", "branch", "technology")
    list_filter = ("branch", "technology", "created_at")
    ordering = ("-created_at",)

# ---------------------------------
# ----------------------------
@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "score", "total_questions", "attempt_date")
    list_filter = ("category", "attempt_date")
    search_fields = ("user__username",)
    ordering = ("-attempt_date",)

# ---------------------

@admin.register(JobPost)
class JobPostAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'job_role', 'category', 'posted_at']

# ================= OTHER MODELS =================
admin.site.register(Choice)
admin.site.register(Resume)
admin.site.register(MaterialCategory)
admin.site.register(StudyMaterial)
admin.site.register(MaterialDownload)
admin.site.register(JobApplication)