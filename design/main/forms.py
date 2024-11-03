from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re
from .models import Claim

class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')
    full_name = forms.CharField(
        label='ФИО',
        max_length=255,
        required=True
    )
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
        if not re.match(r'^[а-яА-Я-]+$', full_name):
            raise ValidationError('ФИО должно содержать только кириллические буквы, дефис и пробелы')
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

class ClaimForm(forms.ModelForm):

    class Meta:
        model = Claim
        fields = ['name', 'description', 'category', 'photo']

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if not photo:
            raise forms.ValidationError('Пожалуйста, загрузите фото.')
        if photo.size > 2 * 1024 * 1024:
            raise forms.ValidationError('Размер фото не должен превышать 2MB.')
        if not photo.name.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            raise forms.ValidationError('Недопустимый формат файла. Используйте jpg, jpeg, png или bmp.')
        return photo

class StatusFilterForm(forms.Form):
    status_choices = (
        ('new', 'Новая'),
        ('accepted', 'Принято в работу'),
        ('completed', 'Выполнено'),
    )
    status = forms.ChoiceField(choices=status_choices, required=False)

class ClaimStatusForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['status', 'comment', 'admin_photo']

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get("status")
        comment = cleaned_data.get("comment")
        admin_photo = cleaned_data.get("admin_photo")

        if self.instance.status in ['accepted', 'completed'] and status == 'new':
            self.add_error('status',
                           'Нельзя изменить статус на "Новая", если он уже "Принято в работу" или "Выполнено".')

        if status == 'accepted' and not comment:
            self.add_error('comment', 'Комментарий обязателен при смене статуса на "Принято в работу".')

        if status == 'completed' and not admin_photo:
            self.add_error('admin_photo', 'Фото обязательно при смене статуса на "Выполнено".')

        return cleaned_data



class PhotoForm(forms.Form):
    photo = forms.ImageField()