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
