from django.urls import path
from .views import RegisterView, CustomLoginView, ProfileView, check_username, CreateClaimView, DeleteClaimView
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', views.index, name='index'),
    path('check-username/', check_username, name='check_username'),
    path('create_claim/', CreateClaimView.as_view(), name='create_claim'),
    path('delete_claim/<int:claim_id>/', DeleteClaimView.as_view(), name='delete_claim'),
]

