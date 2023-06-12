from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

""" User = get_user_model() """

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Informe um email válido.')

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('username')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = user.email  # Use o email como nome de usuário
        if commit:
            user.save()
        return user
