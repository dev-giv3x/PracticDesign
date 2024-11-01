from django.views.generic import CreateView, DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, ClaimForm
from .models import Claim


class DeleteClaimView(View):
    def post(self, request, claim_id):
        claim_instance = get_object_or_404(Claim, id=claim_id, user=request.user)

        if claim_instance.status == 'new':
            claim_instance.delete()
            messages.success(request, 'Заявка успешно удалена.')
        else:
            messages.error(request, 'Ошибка: заявку можно удалить только в статусе "Новая".')

        return redirect('profile')


class CreateClaimView(CreateView):
    model = Claim
    form_class = ClaimForm
    template_name = 'main/create_claim.html'  # Убедитесь, что путь к шаблону правильный

    def form_valid(self, form):
        claim_instance = form.save(commit=False)
        claim_instance.user = self.request.user  # Предположим, что у вас есть связь с пользователем
        claim_instance.save()
        messages.success(self.request, 'Заявка успешно создана.')
        return redirect('profile')  # Предположим, что у вас есть профиль

    def form_invalid(self, form):
        messages.error(self.request, 'Пожалуйста, исправьте ошибки в форме.')
        return self.render_to_response(self.get_context_data(form=form))


def check_username(request):
    username = request.GET.get('username', None)
    is_taken = User.objects.filter(username=username).exists()
    return JsonResponse({'is_taken': is_taken})

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