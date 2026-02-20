from django.urls import path
from .views import *

app_name = 'tasks'

urlpatterns = [
    path('assign/', AssignTaskView.as_view(), name='assign'),
    path('<int:id>', DisplayTaskView.as_view(), name='display')
]