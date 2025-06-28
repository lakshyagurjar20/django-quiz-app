from django import forms
from .models import Question

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
