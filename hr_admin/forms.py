from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models  import User
from .models import CustomUser

class SignupForm(UserCreationForm):

    class Meta(UserChangeForm):
        model=CustomUser
        fields=('name','email','username','role','company','phone','employees','password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    name=forms.CharField(required=True)
    role=forms.CharField(required=True)
    company=forms.CharField(required=True)
    phone=forms.CharField(required=True)
    employees=forms.CharField(required=True)
    email=forms.EmailField(required=True,help_text='Email address')
    class Meta:
        model=CustomUser
        fields=('name','email','username','role','company','phone','employees')

class LoginForm(forms.Form):
    email=forms.CharField(label="Email",required=True)
    password=forms.CharField(label="Password",required=True, widget=forms.PasswordInput)
