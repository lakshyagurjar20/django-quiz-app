from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_selection, name='login_selection'),  # ✅ set new landing page
    path('quiz/', views.quiz, name='quiz'),
    path('result/<int:score>/<int:total>/', views.result, name='result'),
     path('', views.login_selection, name='login_selection'),
    path('student-login/', views.student_login, name='student_login'),
    path('teacher-login/', views.teacher_login, name='teacher_login'),
    path('student-subjects/', views.student_subjects, name='student_subjects'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
     path('quiz/<str:subject>/', views.quiz_by_subject, name='quiz_by_subject'),
    path('quiz/subject-question/', views.quiz_subject_question, name='quiz_subject_question'),
    path('subject/<int:subject_id>/quizzes/', views.quizzes_by_subject, name='quizzes_by_subject'),
    path('quiz/<int:quiz_id>/start/', views.take_quiz, name='take_quiz'),
]
