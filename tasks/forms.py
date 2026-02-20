from django import forms
from .models import *
from django.contrib.auth import get_user_model

User = get_user_model()

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class AssignTaskForm(forms.ModelForm):
    documents = MultipleFileField(required=False)

    assigned_to = forms.ModelChoiceField(
        queryset=User.objects.none(),
        label='Assignee'
    )

    class Meta:
        model = Task
        fields = ['title', 'detail', 'status', 'start_at', 'finish_at', 'assigned_to']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].queryset = User.objects.filter(supervisor=user)

    def clean_assigned_to(self):
        assigned_user = self.cleaned_data.get('assigned_to')
        if not assigned_user:
            raise forms.ValidationError("You must select a user to assign.")
        return assigned_user