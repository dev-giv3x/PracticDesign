from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')
    full_name = forms.CharField(
        label='ФИО',
        max_length=255,
        required=True
    )
    # last_name = forms.CharField(
    #     label='Фамилия',
    #     max_length=255,
    #     required=True
    # )
    # first_name = forms.CharField(
    #     label='Имя',
    #     max_length=255,
    #     required=True
    # )
    # patronymic = forms.CharField(
    #     label='Отчество',
    #     max_length=255,
    #     required=True
    # )
    username = forms.CharField(
        label='Логин',
        max_length=150,
        required=True
    )
    consent = forms.BooleanField(required=True, label='Согласие на обработку персональных данных')
    class Meta:
        model = User
        fields = ('username', 'full_name','email', 'password1', 'password2', 'consent')
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^[a-zA-Z-]+$', username):
            raise ValidationError('Логин должен содержать только латиницу и дефисы.')
        return username
    def clean_full_name(self):
        full_name = self.cleaned_data.get('full_name')
        if not re.match(r'^[a-zA-Z-]+$', full_name):
            raise ValidationError('ФИО должно содержать только кириллические буквы, дефис и пробелы')
    # def clean_last_name(self):
    #     last_name = self.cleaned_data.get('last_name')
    #     if not re.match(r'^[а-яА-ЯёЁА-Я\s-]+$', last_name):
    #         raise ValidationError('Фамилия должна содержать только кириллицу, дефисы и пробелы.')
    #     return last_name
    # def clean_first_name(self):
    #     first_name = self.cleaned_data.get('first_name')
    #     if not re.match(r'^[a-zA-Z-]+$', first_name):
    #         raise ValidationError('ФИО должно содержать только кириллицу, дефисы и пробелы.')
    #     return first_name
    # def clean_patronymic_name(self):
    #     patronymic = self.cleaned_data.get('patronymic')
    #     if not re.match(r'^[a-zA-Z-]+$', patronymic):
    #         raise ValidationError('ФИО должно содержать только кириллицу, дефисы и пробелы.')
    #     return patronymic
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            self.add_error('password2', 'Пароли не совпадают.')
        return cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class PhotoForm(forms.Form):
    photo = forms.ImageField()