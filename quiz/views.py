from django.shortcuts import render, redirect
from .models import Question

def home(request):
    # Clear previous quiz state if any
    if 'question_index' in request.session:
        del request.session['question_index']
    if 'score' in request.session:
        del request.session['score']
    return render(request, 'home.html')

def quiz(request):
    questions = list(Question.objects.all())
    total = len(questions)

    # Initialize session variables at the start
    if 'question_index' not in request.session:
        request.session['question_index'] = 0
        request.session['score'] = 0

    index = request.session['question_index']

    # If quiz is over, redirect to result
    if index >= total:
        score = request.session.get('score', 0)
        # Clear session variables after quiz ends
        del request.session['question_index']
        del request.session['score']
        return redirect('result', score=score, total=total)

    current_question = questions[index]

    if request.method == 'POST':
        selected = request.POST.get('answer')
        if selected and int(selected) == current_question.correct_option:
            request.session['score'] += 1

        # Move to next question
        request.session['question_index'] += 1
        return redirect('quiz')

    return render(request, 'quiz_onebyone.html', {
        'question': current_question,
        'index': index + 1,
        'total': total,
    })

def result(request, score, total):
    return render(request, 'result.html', {'score': score, 'total': total})

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import StudentLoginForm, TeacherLoginForm
from .models import UserProfile, Question

def login_selection(request):
    return render(request, 'login_selection.html')

def student_login(request):
    if request.method == 'POST':
        form = StudentLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'student':
                login(request, user)
                return redirect('student_subjects')
            else:
                form.add_error(None, 'You are not registered as a student.')
    else:
        form = StudentLoginForm()
    return render(request, 'login.html', {'form': form, 'title': 'Student Login'})

def teacher_login(request):
    if request.method == 'POST':
        form = TeacherLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            profile = UserProfile.objects.get(user=user)
            if profile.role == 'teacher':
                login(request, user)
                return redirect('teacher_dashboard')
            else:
                form.add_error(None, 'You are not registered as a teacher.')
    else:
        form = TeacherLoginForm()
    return render(request, 'login.html', {'form': form, 'title': 'Teacher Login'})

from .models import Subject

@login_required
def student_subjects(request):
    subjects = Subject.objects.all()
    return render(request, 'student_subjects.html', {'subjects': subjects})


@login_required
def teacher_dashboard(request):
    return render(request, 'teacher_dashboard.html')

from django.shortcuts import get_object_or_404

@login_required
def quiz_by_subject(request, subject):
    questions = Question.objects.filter(subject=subject)
    total = questions.count()

    if total == 0:
        return render(request, 'no_questions.html', {'subject': subject})

    request.session['question_index'] = 0
    request.session['score'] = 0
    request.session['subject'] = subject

    return redirect('quiz_subject_question')
@login_required
def quiz_subject_question(request):
    subject = request.session.get('subject')
    questions = list(Question.objects.filter(subject=subject))
    total = len(questions)

    index = request.session.get('question_index', 0)

    if index >= total:
        score = request.session.get('score', 0)
        # Clear session vars
        for key in ['question_index', 'score', 'subject']:
            if key in request.session:
                del request.session[key]
        return redirect('result', score=score, total=total)

    current_question = questions[index]

    if request.method == 'POST':
        selected = request.POST.get('answer')
        if selected and int(selected) == current_question.correct_option:
            request.session['score'] += 1

        request.session['question_index'] += 1
        return redirect('quiz_subject_question')

    return render(request, 'quiz_onebyone.html', {
        'question': current_question,
        'index': index + 1,
        'total': total,
    })
@login_required
def quizzes_by_subject(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    quizzes = subject.quizzes.all()
    return render(request, 'quizzes_by_subject.html', {'subject': subject, 'quizzes': quizzes})
from django.shortcuts import render, redirect, get_object_or_404
from .models import Quiz, Question

from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question

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



