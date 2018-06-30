from django import forms
from .models import *

class SubscribeForm(forms.ModelForm):
    email = forms.EmailField(max_length=100, required = True)

    class Meta:
        model = Emails
        fields = ('email', )