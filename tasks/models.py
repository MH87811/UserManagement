from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('success', 'Success'),
        ('failed', 'Failed')
    )

    title = models.CharField(max_length=64)
    detail = models.TextField()
    assigner = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assigner')
    assigned_to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='assignee')
    status = models.CharField(max_length=64, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    start_at = models.DateField()
    finish_at = models.DateField()

    def __str__(self):
        return self.title

def task_document_path(instance, filename):
    return f'tasks/{instance.task.id}/{filename}'

class TaskDocument(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_documents')
    document = models.FileField(upload_to=task_document_path)

    def __str__(self):
        return f'{self.task} - {self.document.name}'
