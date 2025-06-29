from django.db import models


from django.contrib.auth.models import User

class UserProfile(models.Model):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    subject = models.ForeignKey(Subject, related_name='quizzes', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject.name} - {self.title}"
from django.shortcuts import render, get_object_or_404


def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, pk=quiz_id)
    questions = quiz.questions.all().order_by('id')  # Order questions consistently

    current_index = request.session.get(f'quiz_{quiz_id}_current_index', 0)

    if request.method == 'POST':
        selected_option_key = request.POST.get('option')
        current_question_id = request.session.get(f'quiz_{quiz_id}_current_question_id')
        current_question = get_object_or_404(Question, pk=current_question_id)

        selected_answer_text = getattr(current_question, selected_option_key, "")

        # 🟢 Map integer correct_option (1-4) to option field name:
        option_map = {1: "option1", 2: "option2", 3: "option3", 4: "option4"}
        correct_option_key = option_map.get(current_question.correct_option, "")
        correct_answer_text = getattr(current_question, correct_option_key, "")

        if selected_answer_text == correct_answer_text:
            score = request.session.get(f'quiz_{quiz_id}_score', 0) + 1
            request.session[f'quiz_{quiz_id}_score'] = score

        current_index += 1
        request.session[f'quiz_{quiz_id}_current_index'] = current_index

    if current_index >= questions.count():
        score = request.session.get(f'quiz_{quiz_id}_score', 0)
        request.session.pop(f'quiz_{quiz_id}_current_index', None)
        request.session.pop(f'quiz_{quiz_id}_current_question_id', None)
        request.session.pop(f'quiz_{quiz_id}_score', None)
        return render(request, 'quiz_result.html', {'quiz': quiz, 'score': score, 'total': questions.count()})

    current_question = questions[current_index]
    request.session[f'quiz_{quiz_id}_current_question_id'] = current_question.id

    return render(request, 'quiz_question.html', {
        'quiz': quiz,
        'question': current_question,
        'current': current_index + 1,
        'total': questions.count()
    })

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE, null=True, blank=True)

    question_text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)

    correct_option = models.IntegerField(
        choices=[
            (1, 'Option 1'),
            (2, 'Option 2'),
            (3, 'Option 3'),
            (4, 'Option 4')
        ]
    )

    def __str__(self):
        if self.quiz:
            return f"{self.quiz.title}: {self.question_text[:50]}"
        return f"(No Quiz) {self.question_text[:50]}"

    def get_correct_answer_text(self):
        """
        Returns the text of the correct option based on the correct_option integer.
        """
        option_map = {
            1: self.option1,
            2: self.option2,
            3: self.option3,
            4: self.option4
        }
        return option_map.get(self.correct_option, "")



