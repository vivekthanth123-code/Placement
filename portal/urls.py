from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    
    path('upload-resume/', views.upload_resume, name='upload_resume'),
    path('profile/', views.profile, name='profile'),
    path('study-materials/', views.material_categories, name='study_materials'),
    path('jobs/', views.jobs, name='jobs'),
    path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
   
    # ⭐ ADMIN
    path('students/', views.student_list, name='student_list'),
    path('students/delete/<int:pk>/', views.student_delete, name='student_delete'),
    path('students/update/<int:pk>/', views.student_update, name='student_update'),
    path('quiz/', views.quiz_home, name='quiz_home'),
    path('quiz/<slug:slug>/', views.category_quiz, name='category_quiz'),
    path('result/<int:attempt_id>/', views.result, name='result'),
    path('materials/', views.material_categories, name='material_categories'),
    path('materials/<int:category_id>/', views.material_list, name='material_list'),
    path('download/<int:material_id>/', views.download_material, name='download_material'),
     
]