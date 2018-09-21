from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ['user']

    first_name = forms.CharField(max_length=90)
    last_name = forms.CharField(max_length=90)