from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CustomUserCreationForm
from django.contrib import messages
from .forms import RequestForm
from .models import Request

def user_login(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Неверное имя пользователя или пароль')
    else:
        form = LoginForm()

    return render(request, 'user/login.html', {'form': form})

def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('index')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Вы успешно зарегистрированы! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'user/register.html', {'form': form})


def profile(request):
    status = request.GET.get('status')

    if status:
        user_requests = Request.objects.filter(user=request.user, status=status)
    else:
        user_requests = Request.objects.filter(user=request.user)

    return render(request, 'user/profile.html', {
        'user_requests': user_requests,
        'selected_status': status
    })


def create_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST, request.FILES)
        if form.is_valid():
            request_instance = form.save(commit=False)
            request_instance.user = request.user
            request_instance.save()
            return redirect('profile')
    else:
        form = RequestForm()

    return render(request, 'user/create_request.html', {
        'form': form
    })

def delete_request(request, request_id):
    request_instance = get_object_or_404(Request, id=request_id, user=request.user)

    if request_instance.status == 'new':
        request_instance.delete()
        messages.success(request, 'Заявка успешно удалена.')
    else:
        messages.error(request, 'Ошибка: заявку можно удалить только в статусе "Новая".')

    return redirect('profile')