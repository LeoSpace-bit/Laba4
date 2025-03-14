"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm

from Laba4 import settings
from .forms import AnketaForm, CommentForm, BlogForm
from django.db import models
from .models import Blog

from .models import Comment

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Домой',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Контакты для тебя',
            'year':datetime.now().year,
        }
    )

def about(request):
    print(settings.MEDIA_ROOT)
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Твоё приложение.',
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Я телевизор',
            'year':datetime.now().year,
        }
    )

def links (request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Кофе',
            'message':'Кофе много не бывает',
            'year':datetime.now().year,
        }
    )

def anketa(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    internet = {'1': 'Каждый день', '2': 'Несколько раз в день',
                '3': 'Несколько раз в неделю', '4': 'Несколько раз в месяц'}
    if request.method == "POST":
        form = AnketaForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['job'] = form.cleaned_data['job']
            data['gender'] = gender[form.cleaned_data['gender']]
            data['internet'] = internet[form.cleaned_data['internet']]
            if form.cleaned_data['notice']:
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['message'] = form.cleaned_data['message']
            form = None
    else:
        form = AnketaForm()
    return render(
        request,
        'app/anketa.html',
        {
            'form': form,
            'data': data
        }
    )


def registration(request):
    """Renders the registration page."""
    if request.method == "POST":
        regform = UserCreationForm(request.POST)  # после отправки формы
        if regform.is_valid():
            reg_f = regform.save(commit=False)  # запрещаем ввод в админстративный раздел
            reg_f.is_staff = False
            reg_f.is_active = True  # активный пользователь
            reg_f.is_superuser = False  # не является суперпользователем
            reg_f.date_joined = datetime.now()  # дата регистрации
            reg_f.last_login = datetime.now()  # дата последней авторизации

            regform.save()  # сохранение изменений после добавления полей регистрации
            return redirect('home')  # перенаправление на главную страницу после регистрации
    else:
        regform = UserCreationForm()  # создание объекта формы для ввода данных

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,  # передача формы в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )


def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()  # Запрос на выбор всех статей блога из модели

    import subprocess
    with open("requirements2.txt", "w") as f:
        subprocess.run(["pip", "freeze"], stdout=f)


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title': 'Блог',
            'posts': posts,  # Передача списка статей в шаблон веб-страницы
            'year': datetime.now().year,
        }
    )


def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)  # Запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()
        
    


    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,  # Передача конкретной статьи в шаблон веб-страницы
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )


def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)  # после отправки формы
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()  # сохраняем изменения после добавления полей

            return redirect('blog')  # переадресация на страницу Блог после создания статьи Блога
    else:
        blogform = BlogForm()  # создание объекта формы для ввода данных

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,  # передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            'year': datetime.now().year,
        }
    )
