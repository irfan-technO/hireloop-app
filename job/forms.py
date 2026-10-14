from django import forms
from .models import Job, JobRes, JobExp

class CreateJobForms(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('company', 'date_time_posted', 'date_posted', 'is_published', 'expiry_date')

class UpdateJobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('company', 'date_time_posted', 'date_posted', 'is_published', 'expiry_date' )

class AddJobRes(forms.ModelForm):
    class Meta:
        model = JobRes
        fields = ['name']

class AddJobExp(forms.ModelForm):
    class Meta:
        model = JobExp
        fields = ['name']