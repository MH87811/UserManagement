from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import *


# Create your views here.

def DashboardView(request):
    return render(request, 'dashboard.html')

class Register_View(FormView):
    template_name = 'users/register.html'
    form_class = Registration_Form

    success_url = reverse_lazy('users:dashboard')
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'registered successfully')
        return super().form_valid(form)

class Login_View(LoginView):
    template_name = 'users/login.html'
    from_classes = Login_Form
    success_url = reverse_lazy('users:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:dashboard')
        return super().dispatch(request, *args, **kwargs)

class Logout_View(LogoutView):
    next_page = reverse_lazy('users:login')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = Profile_UpdateForm
    template_name = 'users/profile_update.html'

    success_url = reverse_lazy('users:profile')
    def get_queryset(self):
        return Profile.objects.get(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, 'profile updated')
        return super().form_valid(form)

class ProfileView(LoginRequiredMixin, ListView):
    template_name = 'users/profile_detail.html'
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)
        return context

class DisplayProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile_detail.html'

    def get_object(self):
        pk = self.kwargs['id']
        return get_object_or_404(Profile, id=pk)