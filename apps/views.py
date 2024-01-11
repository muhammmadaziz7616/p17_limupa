from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from apps.forms import RegisterForm
from apps.models import Blog, Comment


def index(request):
    return render(request, 'apps/index.html')


def login_register(request):
    return render(request, 'apps/login_register.html')


def blog_list_page(request):
    context = {
        'blogs': Blog.objects.all(),
        'commernts': Comment.objects.all()
    }
    return render(request, 'apps/blogs/blog-list.html', context)


def blog_detail_page(request):
    context = {
        'blogs': Blog.objects.all()
    }
    return render(request, 'apps/blogs/blog-detail.html', context)


def index_page(request):
    return render(request, 'apps/index.html')


def logout_page(request):
    logout(request)
    return redirect('index_page')


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('index')
    return render(request, 'apps/login_register.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.save()
            return redirect('index')
    else:
        form = RegisterForm()

    context = {'form': form}
    return render(request, 'apps/login_register.html', context)
