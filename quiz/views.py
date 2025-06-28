from django.shortcuts import render, redirect
from .models import Question

def home(request):
    return render(request, 'home.html')

def quiz(request):
    if request.method == 'POST':
        questions = Question.objects.all()
        score = 0
        total = questions.count()
        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option and int(selected_option) == question.correct_option:
                score += 1
        return redirect('result', score=score, total=total)
    else:
        questions = Question.objects.all()
        return render(request, 'quiz.html', {'questions': questions})

def result(request, score, total):
    return render(request, 'result.html', {
        'score': score,
        'total': total,
    })
