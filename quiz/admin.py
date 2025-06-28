from django.contrib import admin
from .models import Subject, Quiz, Question

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 1

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [QuizInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject')
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz')
