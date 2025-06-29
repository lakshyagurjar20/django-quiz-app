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
     # Teacher dashboard & subject view
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/subject/<int:subject_id>/', views.teacher_subject_detail, name='teacher_subject_detail'),

    # Quiz CRUD for teachers
    path('teacher/subject/<int:subject_id>/quiz/add/', views.add_quiz, name='add_quiz'),
    path('teacher/quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('teacher/quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),

    # Question CRUD for teachers
    path('teacher/quiz/<int:quiz_id>/question/add/', views.add_question, name='add_question'),
    path('teacher/question/<int:question_id>/edit/', views.edit_question, name='edit_question'),
    path('teacher/question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
     path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/subject/<int:subject_id>/quiz/add/', views.quiz_form, name='teacher_add_quiz'),
    path('teacher/subject/<int:subject_id>/quiz/<int:quiz_id>/edit/', views.quiz_form, name='teacher_edit_quiz'),
    path('teacher/quiz/<int:quiz_id>/question/add/', views.question_form, name='teacher_add_question'),
    path('teacher/quiz/<int:quiz_id>/question/<int:question_id>/edit/', views.question_form, name='teacher_edit_question'),
    

]
