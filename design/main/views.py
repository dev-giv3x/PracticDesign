from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Claim


class CustomLoginView(LoginView):
    template_name = 'authorization/login.html'

    def form_valid(self, form):
        messages.success(self.request, "Вы успешно вошли в систему.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Неправильный логин или пароль.")
        return super().form_invalid(form)


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'authorization/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        messages.success(self.request, "Регистрация прошла успешно.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "Пожалуйста, исправьте ошибки в форме.")
        return super().form_invalid(form)

class ProfileView(View):
    def get(self, request, *args, **kwargs):
        status = request.GET.get('status')

        if status:
            user_requests = Claim.objects.filter(user=request.user, status=status)
        else:
            user_requests = Claim.objects.filter(user=request.user)

        return render(request, 'authorization/profile.html', {
            'user_requests': user_requests,
            'selected_status': status
        })

def index(request):
    return render(request, 'index.html')