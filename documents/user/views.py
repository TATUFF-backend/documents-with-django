from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import LoginForm


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('main:home')
        context = {
            'form': LoginForm(),
            'title': 'Sign in',
        }
        return render(request, 'user/login.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            return redirect('shop:home')
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            to = request.GET.get('next', 'main:home')
            return redirect(to)
        else:
            context = {
                'form': form,
                'title': 'Kirish',
            }
            return render(request, 'user/login.html', context)


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('main:home')
