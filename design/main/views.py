from django.views.generic import CreateView, DetailView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistrationForm, ClaimForm
from django.contrib.auth.decorators import login_required
from .models import Claim, Category


def index(request):
    completed_requests = Claim.objects.filter(status='completed').order_by('-created_time')[:4]

    accepted_requests_count = Claim.objects.filter(status='accepted').count()

    context = {
        'completed_requests': completed_requests,
        'accepted_requests_count': accepted_requests_count,

    }
    return render(request, 'index.html', context)

def create_claim(request):
    categories = Category.objects.all()
    form = ClaimForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('profile')
    return render(request, 'main/create_claim.html', {'form': form, 'categories': categories})

class DeleteClaimView(View):
    def get(self, request, claim_id):
        claim_instance = get_object_or_404(Claim, id=claim_id, user=request.user)
        return render(request, 'main/delete_claim.html', {'claim': claim_instance})

    def post(self, request, claim_id):
        claim_instance = get_object_or_404(Claim, id=claim_id, user=request.user)

        if claim_instance.status == 'new':
            claim_instance.delete()
            return redirect('profile')
        else:
            return redirect('profile')
class CreateClaimView(CreateView):
    model = Claim
    form_class = ClaimForm
    template_name = 'main/create_claim.html'

    def form_valid(self, form):
        claim_instance = form.save(commit=False)
        claim_instance.user = self.request.user
        claim_instance.save()
        return redirect('profile')

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
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class RegisterView(CreateView):
    form_class = RegistrationForm
    template_name = 'authorization/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password1'])
        user.save()
        return super().form_valid(form)

    def form_invalid(self, form):
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
