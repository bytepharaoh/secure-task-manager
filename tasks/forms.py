from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title' , 'description' ,'priority' , 'due_date']
        widgets={
            'due_date':forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if not title:
            raise forms.ValidationError("Title is required.")
        return title

    def clean(self):
        cleaned_data = super().clean()
        due_date = cleaned_data.get("due_date")
        if due_date and due_date.year < 2000:
            self.add_error("due_date", "Due date must be a valid modern date.")
        return cleaned_data
