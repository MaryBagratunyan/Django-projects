from django.urls import reverse
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password

from .forms import RegisterForm


class RegisterView(FormView):
    def get(self, request):
        return render(request, 'core/register.html', {'form': RegisterForm})

    def post(self, request):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user['password'] = make_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect(reverse('dashboard-view'))
        return render(request, 'core/register.html', {'form': RegisterForm})

