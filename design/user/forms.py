from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
import re
from .models import Request, Category, CustomUser

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
        }),
        label='Имя пользователя'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
        }),
        label='Пароль'
    )

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'email', 'password1', 'password2', 'consent', 'district')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z-]+$', username):
            raise ValidationError('Логин должен содержать только латиницу и дефисы.')
        return username

    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[а-яА-ЯёЁА-Я\s-]+$', full_name):
            raise ValidationError('ФИО должно содержать только кириллицу, дефисы и пробелы.')
        return full_name

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['title', 'description', 'category', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            if photo.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError('Размер фото не должен превышать 2MB.')
            if not photo.name.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                raise forms.ValidationError('Недопустимый формат файла. Используйте jpg, jpeg, png или bmp.')
        return photo