from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Имя пользователя'
        })
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Введите пароль'
        })
    )


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Имя пользователя',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Введите имя пользователя'
        })
    )

    avatar = forms.ImageField(
        label='Аватар',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control'
        })
    )

    email = forms.EmailField(
        label='Почта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control', 'placeholder': 'Введите почту'
        })
    )

    phone = forms.CharField(
        label='Телефон',
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': '+998(90)123-45-67'
        })
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Введите пароль'
        })
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'avatar', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            user.avatar = avatar
        if commit:
            user.save()
        return user

