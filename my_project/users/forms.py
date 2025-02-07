from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2', 'avatar', 'phone_number', 'country')

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label='Email')
