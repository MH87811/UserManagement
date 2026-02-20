from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import *
from .forms import *

# Create your views here.


class AssignTaskView(CreateView, LoginRequiredMixin):
    model = Task
    form_class = AssignTaskForm
    template_name = 'tasks/assign_task.html'
    success_url = reverse_lazy('users:dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        assigned_user = form.cleaned_data['assigned_to']
        current_user = self.request.user
        if assigned_user.supervisor == current_user or current_user.is_admin:
            form.instance.assigner = current_user
            response = super().form_valid(form)
            for file in self.request.FILES.getlist('documents'):
                TaskDocument.objects.create(task=self.object, document=file)

            return response
        raise PermissionDenied("You cannot assign task to this user.")


class DisplayTaskView(DetailView, LoginRequiredMixin):
    model = Task
    template_name = 'tasks/display_task.html'

    def get_object(self):
        id = self.kwargs['id']
        return get_object_or_404(Task, id=id, assigned_to=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task_id = self.kwargs['id']
        context['documents'] = TaskDocument.objects.filter(task=task_id)
        return context