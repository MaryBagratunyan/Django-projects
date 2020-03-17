from django.urls import reverse
from django.views.generic.edit import FormView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect

from .models import User
from .forms import RegisterForm, LoginForm
from questans.models import Question, Answer, QuestionGroups


class RegisterView(FormView):
    def get(self, request):
        return render(request, 'core/register.html', {'form': RegisterForm})

    def post(self, request):
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect(reverse('dashboard'))
        return render(request, 'core/register.html', {'form': RegisterForm})


class DashboardView(FormView):
    def get(self, request):
        if request.user.is_authenticated:
            content = {}
            user = request.user
            user.backend = 'django.contrib.core.backends.ModelBackend'
            ques_obj = Question.objects.filter(user=user)
            content['userdetail'] = user
            content['questions'] = ques_obj
            if ques_obj:
                ans_obj = Answer.objects.filter(question=ques_obj[0])
            else:
                ans_obj = []
            content['answers'] = ans_obj
            return render(request, 'core/dashboard.html', content)
        else:
            return redirect(reverse('login'))


class LoginView(FormView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect(reverse('dashboard'))
        return render(request, 'core/login.html', {'form': LoginForm})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        try:
            users = User.objects.filter(email=email)
            user = authenticate(request, username=users.first().username, password=password)
            login(request, user)
            return redirect(reverse('dashboard'))
        except Exception as e:
            content = {'form': LoginForm, 'error': 'Unable to login with provided credentials ' + str(e)}
            return render(request, 'core/login.html', content)


class LogoutView(FormView):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect('/')
