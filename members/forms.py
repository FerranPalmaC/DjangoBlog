from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from members.models import CustomUser
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = CustomUser 
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]


class LoginForm(AuthenticationForm):
      
    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['username'].label = 'Username/Email'
