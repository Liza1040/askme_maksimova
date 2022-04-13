from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib import auth
from django.http import HttpResponse

from app.models import *


def paginate(objects, request, per_page=20):
    paginator = Paginator(objects, per_page)
    page = request.GET.get('page')
    try:
        result_page = paginator.page(page)
    except PageNotAnInteger:
        result_page = paginator.page(1)
    except EmptyPage:
        result_page = paginator.page(paginator.num_pages)
    return result_page

def index(request):
    questions = paginate(Question.objects.get_new(), request)
    if questions is None:
        raise Http404
    return render(request, 'index.html', {
        'questions': questions
    }
                  )

def logout(request):
    auth.logout(request)
    url = request.GET.get('next', '/')
    return redirect(url)

def tag(request, pk):
    received_tag = Tag.objects.get_by_tag(pk)
    if received_tag is None:
        return render(request, 'tag.html', {
            'tag': pk
        }
                      )
    question_tag = paginate(received_tag, request)
    if question_tag is None:
        raise Http404
    return render(request, 'tag.html', {
        'tag': pk,
        'questions': question_tag
    }
                  )

def hot(request):
    hot_questions = paginate(Question.objects.get_hot(), request)
    if hot_questions is None:
        raise Http404

    return render(request, 'hot.html', {
        'questions': hot_questions
    }
                  )

def one_question(request, pk):
    selected_question = Question.objects.get_by_id(pk).first()
    print(selected_question)
    if selected_question is None:
        raise Http404
    answer = paginate(Answer.objects.get_answer(pk), request)
    answers_count = Answer.objects.get_count_answer(pk)
    return render(request, 'question.html', {
        'question': selected_question,
        'answers_count': answers_count,
        'answers': answer
        # 'form': form
    }
                  )

def ask(request):
    return render(request, "ask.html")

def question(request):
    return render(request, "question.html", {})

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "signup.html")

def settings(request):
    return render(request, "user.html")

# def tag(request, t):
#     return render(request, "tag.html", {"tag": t, "questions": QUESTIONS})

# def hot(request):
#     return render(request, "hot.html", {"questions": QUESTIONS})