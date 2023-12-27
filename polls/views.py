from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django import forms
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout

from .models import Choice, Question

def logout(request):
    logout(request)
    return redirect('login')

def login(request):
    return render(request, 'polls/login.html')

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

class AddQuestionForm(forms.Form):
    question = forms.CharField(max_length=200)
    choice1 = forms.CharField(max_length=200)
    choice2 = forms.CharField(max_length=200)

@csrf_exempt # 1. Remove decorator, uncomment csrf-middleware in settings.py and uncomment csrf-token in index.html
def addquestion(request):
    #if request.method == 'POST':
        #form = AddQuestionForm(request.POST)
        #if form.is_valid():
    question = request.GET.get("q")
    choice1 = request.GET.get("c1")
    choice2 = request.GET.get("c2")

    q = Question(question_text=question, pub_date=datetime.now())
    q.save()
    q.choice_set.create(choice_text=choice1, votes=0)
    q.choice_set.create(choice_text=choice2, votes=0)
    q.save()
    form = AddQuestionForm()
    return HttpResponseRedirect(reverse('index'))

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('results', args=(question.id,)))