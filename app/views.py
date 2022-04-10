from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
QUESTIONS = [
    {
        "title": f"Title #{i}",
        "text": f"This is text for question #{i}",
        "number": i,
    } for i in range(20)
]
def index(request):
    return render(request, "index.html", {"questions": QUESTIONS})

def ask(request):
    return render(request, "ask.html")

def question(request, i: int):
    return render(request, "question_page.html", {"question": QUESTIONS[i]})

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "signup.html")

def settings(request):
    return render(request, "user.html")

def tag(request, t):
    return render(request, "questions_by_tag.html", {"tag": t, "questions": QUESTIONS})

def hot(request):
    return render(request, "hot.html", {"questions": QUESTIONS})