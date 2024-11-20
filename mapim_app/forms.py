# forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Historial

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class LoginForm(forms.Form):
    username = forms.CharField(label="Correo Electrónico")
    password = forms.CharField(widget=forms.PasswordInput)


# mapim_app/forms.py


class HistorialForm(forms.ModelForm):
    class Meta:
        model = Historial
        fields = ['paciente', 'imagen', 'resultado', 'realizado_por', 'comentarios']
