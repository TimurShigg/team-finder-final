# projects/forms.py
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'github_url', 'status']

    def clean_github_url(self):
        url = self.cleaned_data.get('github_url')
        if url and not url.startswith('https://github.com/'):
            raise forms.ValidationError("Ссылка должна вести на GitHub (https://github.com/...)")
        return url
