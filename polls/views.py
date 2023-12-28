from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django import forms
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Choice, Question

@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

#@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

#@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

class AddQuestionForm(forms.Form):
    question = forms.CharField(max_length=200)
    choice1 = forms.CharField(max_length=200)
    choice2 = forms.CharField(max_length=200)

#@login_required
@csrf_exempt #Fix 1: Remove this decorator
def addquestion(request):
    if request.method == "GET":         #Fix 2: Change GET to POST
        question = request.GET.get("q") #Fix 2: Change GET to POST
        choice1 = request.GET.get("c1") #Fix 2: Change GET to POST
        choice2 = request.GET.get("c2") #Fix 2: Change GET to POST

        q = Question(question_text=question, pub_date=datetime.now())
        q.save()
        q.choice_set.create(choice_text=choice1, votes=0)
        q.choice_set.create(choice_text=choice2, votes=0)
        q.save()
        return HttpResponseRedirect(reverse('index'))

#@login_required
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