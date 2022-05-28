from django.forms import model_to_dict
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.urls import reverse
from django.db.models import F
from django.views.decorators.http import require_http_methods, require_POST

from app.forms import *


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
    if selected_question is None:
        raise Http404
    answer = paginate(Answer.objects.get_answer(pk), request)
    answers_count = Answer.objects.get_count_answer(pk)

    if (request.method == 'GET'):
        user_form = AnswerForm()
    elif request.method == 'POST':
        form = AnswerForm(data=request.POST)
        if form.is_valid():
            new_answer = form.save(commit=False)
            new_answer.author = request.user
            new_answer.question = selected_question
            new_answer.save()
            return redirect(reverse('question', kwargs={"pk": pk}) + '#answer' + str(new_answer.id))
    return render(request, 'question.html', {
        'question': selected_question,
        'answers_count': answers_count,
        'answers': answer,
        'form': user_form})


@login_required
def ask(request):
    if (request.method == 'GET'):
        user_form = QuestionForm()
    elif request.method == 'POST':
        user_form = QuestionForm(data=request.POST)
        if user_form.is_valid():
            new_question = user_form.save(commit=False)
            new_question.author = request.user
            new_question.save()
            tags = user_form.clean()['tag']

            tags = tags.replace(' ', '')
            parsed_tag = []
            while tags.find(',') != -1:
                one_tag = tags[:tags.find(',')]
                parsed_tag.append(one_tag)
                tags = tags[tags.find(',') + 1:]

            if tags:
                parsed_tag.append(tags)

            new_tags = []
            for one_tag in parsed_tag:
                check_tag = Tag.objects.get_tag(one_tag)
                if check_tag is None:
                    check_tag = Tag.objects.create(text=one_tag)
                new_tags.append(check_tag.id)
            new_question.tag.set(new_tags)
            return redirect(reverse('question', kwargs={"pk": new_question.pk}))
    return render(request, "ask.html", {'form': user_form})


def question(request):
    return render(request, "question.html", {})


def login(request):
    error = ''
    if(request.method == 'GET'):
        user_form = LoginForm()
    elif request.method == 'POST':
        user_form = LoginForm(data=request.POST)
        if user_form.is_valid():
            user = auth.authenticate(request, **user_form.cleaned_data)
            if user:
                auth.login(request, user)
                url = request.GET.get('next','/')
                return redirect(url)
            else:
                error = 'Sorry, wrong login or password'
    return render(request, "login.html", {'error': error,
                                          'form': user_form})


def register(request):
    error = []
    if (request.method == 'GET'):
        user_form = RegisterForm()
    elif request.method == 'POST':
        user_form = RegisterForm(data=request.POST, auto_id=False)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.username = user_form.cleaned_data['login']
            new_user.email = user_form.cleaned_data['email']
            new_user.first_name = user_form.cleaned_data['first_name']
            new_user.last_name = user_form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_user.profile.nickname = user_form.cleaned_data['nickname']
            auth.login(request, new_user)
            return redirect(reverse('new'))
        else:
            for err in user_form.errors['__all__']:
                error.append(err)
    return render(request, "signup.html", {'error': error,
                                           'form': user_form})


@login_required
def settings(request, pk):
    error = []
    if request.method == 'POST':
        user = User.objects.get(id=Profile.objects.get(nickname=pk).user.id)
        user_form = SettingsForm(data=request.POST, files=request.FILES, instance=user)
        if user_form.is_valid():
            new_settings = user_form.save(commit=False)
            if user_form.cleaned_data['email']:
                new_settings.email = user_form.cleaned_data['email']
            if user_form.cleaned_data['first_name']:
                new_settings.first_name = user_form.cleaned_data['first_name']
            if user_form.cleaned_data['last_name']:
                new_settings.last_name = user_form.cleaned_data['last_name']
            new_settings.save()
            new_profile = Profile.objects.get(user=request.user)
            if user_form.cleaned_data['nickname']:
                new_profile.nickname = user_form.cleaned_data['nickname']
            if user_form.cleaned_data['avatar']:
                new_profile.avatar = user_form.cleaned_data['avatar']
            new_profile.save()
            return redirect(reverse('edit', kwargs={"pk": new_profile.nickname}))
        else:
            for err in user_form.errors['__all__']:
                error.append(err)
    else:
        initial_data = model_to_dict(request.user)
        initial_data['avatar'] = request.user.profile.avatar
        initial_data['nickname'] = request.user.profile.nickname
        user_form = SettingsForm(initial=initial_data)
    return render(request, 'user.html', {
        'nickname': pk,
        'form': user_form,
        'error': error
    })


@login_required
@require_POST
def vote(request):
    data = request.POST
    qid = data['qid']
    action = data['action']
    q = Question.objects.get(pk=qid)
    inc = Like.ACTION[action]
    grade = Like.objects.get_like_by_content(ContentType.objects.get_for_model(q), qid, request.user)
    if grade:
        if inc == grade.rating:
            return JsonResponse({'status': 'already voted', 'rating': q.rating})
        else:
            q.rating = F('rating') + inc
            grade.rating = inc
            q.save()
            grade.save()
            q.refresh_from_db()
            return JsonResponse({'status': 'changed', 'rating': q.rating})
    like = Like.objects.create(user=request.user,
                               content_type=ContentType.objects.get_for_model(q),
                               rating=inc, object_id=qid)
    like.save()
    q.rating = F('rating') + inc
    q.save()
    q.refresh_from_db()
    return JsonResponse({'status': 'ok', 'rating': q.rating})


@login_required
@require_POST
def vote_answer(request):
    data = request.POST
    aid = data['aid']
    action = data['action']
    a = Answer.objects.get(pk=aid)
    inc = Like.ACTION[action]
    grade = Like.objects.get_like_by_content(ContentType.objects.get_for_model(a), aid, request.user)

    if grade:
        if inc == grade.rating:
            return JsonResponse({'status': 'already voted', 'rating': a.rating})
        else:
            a.rating = F('rating') + inc
            grade.rating = inc
            a.save()
            grade.save()
            a.refresh_from_db()
            return JsonResponse({'status': 'changed', 'rating': a.rating})
    like = Like.objects.create(user=request.user,
                               content_type=ContentType.objects.get_for_model(a),
                               rating=inc, object_id=aid)
    like.save()
    a.rating = F('rating') + inc
    a.save()
    a.refresh_from_db()

    return JsonResponse({'status': 'ok', 'rating': a.rating})


@login_required
@require_POST
def vote_correct(request):
    data = request.POST
    aid = data['aid']
    qid = data['qid']
    incorrect = ''
    for e in Answer.objects.get_answer(qid):
        if e.correct and e.id != aid:
            e.correct = False
            e.save()
            incorrect = e.id
            break
    a = Answer.objects.get(pk=aid)
    if a.correct:
        a.correct = False
    else:
        a.correct = True
    a.save()
    a.refresh_from_db()

    return JsonResponse({'status': 'ok', 'correct': a.correct, 'incorrect': incorrect})
