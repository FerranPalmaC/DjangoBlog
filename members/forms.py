from django import forms
from django.contrib.auth.forms import UserCreationForm

from members.models import CustomUser

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser 
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
