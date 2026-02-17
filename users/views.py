from django.shortcuts import render
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import *


# Create your views here.

class Register_View(FormView):
    template_name = 'users/register.html'
    form_class = Registration_Form
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'registered successfully')
        return super().form_valid(form)

class Login_View(LoginView):
    template_name = 'users/login.html'
    from_classes = Login_Form
    def get_success_url(self):
        return reverse_lazy('dashboard')

class Logout_View(LogoutView):
    next_page = reverse_lazy('login')

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_classes = Profile_UpdateForm
    template_name = 'users/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.profile

def DashboardView(request):
    return render(request, 'dashboard.html')