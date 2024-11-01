from django.db import models
# from django import forms
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, help_text='Добавьте категорию')

    def __str__(self):
        return self.name


class Claim(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ManyToManyField(Category, help_text="Выберите категорию")
    photo = models.ImageField(upload_to='photos/', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f'{self.name}, {self.category}')

    LOAN_STATUS = (
        ('n', 'Новая'),
        ('a', 'Принято в работу'),
        ('c', 'Выполнено'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='n', help_text='Выберите категорию')