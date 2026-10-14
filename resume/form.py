import datetime
from django import forms
from .models import Education, Resume, Work

# Generate year choices (current year down to 1970)
YEAR_CHOICES = [('', 'Select Year')] + [(str(year), str(year)) for year in range(datetime.datetime.now().year, 1969, -1)]

class AddResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ('user',)
        

class UpdateResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ('user',)

class AddEducationForm(forms.ModelForm):
    school_name = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'e.g. Stanford University'})
    )
    start_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    end_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)

    class Meta:
        model = Education
        fields = ['degree_type', 'course', 'start_year', 'end_year', 'still_in_clg', 'description']

class UpdateEducationForm(forms.ModelForm):
    start_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    end_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)

    class Meta:
        model = Education
        exclude = ('resume',)
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter description...'}),
        }

class AddWorkForm(forms.ModelForm):
    class Meta:
        model = Work
        exclude = ('resume',)
    start_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    end_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)     

class UpdateWorkForm(forms.ModelForm):
    class Meta:
        model = Work
        exclude = ('resume',)