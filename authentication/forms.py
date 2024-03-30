from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class CustomUserCreationForm(UserCreationForm):
    # Agregar clases personalizadas a los campos
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'password'}))

    class Meta:
        model = UserCreationForm
        fields = UserCreationForm.Meta.fields
