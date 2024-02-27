from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect


def login_user(request):
    if request.method == 'POST':
        form_user = AuthenticationForm(data=request.POST)
        if form_user.is_valid():
            user = form_user.get_user()
            login(request, user)
            messages.success(request, f'Вы были успешно авторизованы. Здравствуйте, {user.username}!')

            if request.GET.get('next'):
                return redirect(request.GET.get('next'))

            return redirect('home')
        else:
            messages.warning(request, 'Перепроверьте вводимы данные')
    else:
        form_user = AuthenticationForm()

    context = {
        'form': form_user,
    }
    return render(request, 'auth/login.html', context)


def reg_user(request):
    if request.method == 'POST':
        form_user = UserCreationForm(request.POST)
        if form_user.is_valid():
            user = form_user.save()
            login(request, user)
            messages.info(request, f'Вы были успешно зарегистрированы. Здравствуйте, {user.username}!')
            return redirect('home')
        else:
            messages.warning(request, 'Перепроверьте вводимы данные')
    else:
        form_user = UserCreationForm()

    context = {
        "form": form_user,
    }

    return render(request, 'auth/registration.html', context)


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли из аккаунта')
    return redirect('home')
