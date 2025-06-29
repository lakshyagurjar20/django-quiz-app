from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Quiz, Question

# ✅ Form for students to take a quiz
class QuizForm(forms.Form):
    def __init__(self, *args, **kwargs):
        questions = kwargs.pop('questions')
        super(QuizForm, self).__init__(*args, **kwargs)

        for question in questions:
            self.fields[str(question.id)] = forms.ChoiceField(
                label=question.question_text,
                choices=[
                    ('1', question.option1),
                    ('2', question.option2),
                    ('3', question.option3),
                    ('4', question.option4),
                ],
                widget=forms.RadioSelect,
                required=True,
            )

# ✅ Forms for login
class StudentLoginForm(AuthenticationForm):
    pass  # Uses Django's built-in username & password

class TeacherLoginForm(AuthenticationForm):
    pass  # Uses Django's built-in username & password

# ✅ Form for teachers to add/edit a quiz (only needs title)
class QuizModelForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']

# ✅ Form for teachers to add/edit a question
class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option']

from .models import Quiz, Question

class QuizModelForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title']

class QuestionModelForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question_text', 'option1', 'option2', 'option3', 'option4', 'correct_option']
