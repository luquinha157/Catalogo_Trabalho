from django import forms
from django.contrib.auth.models import User

class LoginForms(forms.Form):
    email = forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        widget=forms.EmailInput(
            attrs={
                'type': "email",
            }
        )
    )
    senha = forms.CharField(
        label='Senha',
        required=True,
        max_length=70,
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
            }
        ),
    )


class UserForms(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input'})),
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'custom-input'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'custom-input'}),
            'email': forms.TextInput(attrs={'class': 'custom-input'}),
            'password': forms.PasswordInput(attrs={'class': 'custom-input'}),
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Senhas não são iguais')

        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_staff = 1
        if commit:
            user.save()
        return user

class RegisterForms(forms.Form):
    email = forms.EmailField(
        label='Email',
        required=True,
        max_length=100,
        widget=forms.EmailInput(attrs={'type': 'email'}),
    )
    username = forms.CharField(
        label='Username',
        required=True,
        max_length=30,
        widget=forms.TextInput(attrs={'type': 'text'}),
    )
    password = forms.CharField(
        label='Senha',
        required=True,
        max_length=100,
        widget=forms.PasswordInput(attrs={'type': 'password'}),
    )
    password_confirm = forms.CharField(
        label='Confirmar Senha',
        required=True,
        max_length=100,
        widget=forms.PasswordInput(attrs={'type': 'password'}),
    )


    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Senhas não são iguais')

        return password_confirm