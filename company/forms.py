from django import forms
from .models import Company
from datetime import datetime

def possible_years(first_year_in_scroll, last_year_in_scroll):
    p_year = []
    for i in range(first_year_in_scroll, last_year_in_scroll, -1):
        p_year.append((i, i))
    return p_year

class AddCompanyForm(forms.ModelForm):
    founded_in = forms.ChoiceField(choices=possible_years(datetime.now().year, 1990))

    class Meta:
        model = Company
        exclude = ('user',)

class UpdateCompanyForm(forms.ModelForm):
    founded_in = forms.ChoiceField(choices=possible_years(datetime.now().year, 1990))

    class Meta:
        model = Company
        fields = [
            'name', 'email_address', 'phone_number', 'website',
            'primary_industry', 'company_size', 'founded_in',
            'state', 'country', 'linkedin', 'twitter', 'about_company'
        ]