from django.contrib import admin
from .models import Subject, Quiz, Question

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class QuizInline(admin.StackedInline):
    model = Quiz
    extra = 1
    show_change_link = True  # shows clickable link to Quiz edit page

class SubjectAdmin(admin.ModelAdmin):
    inlines = [QuizInline]

class QuizAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Quiz, QuizAdmin)  # register QuizAdmin separately

# 🚨 No need to register Question directly
