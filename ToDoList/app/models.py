from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Todo(models.Model):
    PRIORITY = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий'),
    ]

    STATUS = [
        ('done', 'Выполнено'),
        ('not_done', 'Не выполнено'),
    ]

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    description = models.TextField(blank=True, verbose_name='Описание')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создание')
    deadline = models.DateTimeField(verbose_name='Деадлайн')
    priority = models.CharField(max_length=10, choices=PRIORITY, default='medium', verbose_name='Приоритет')
    status = models.CharField(max_length=10, choices=STATUS, default='not_done', verbose_name='Статус')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='todos', verbose_name='Владелец')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.title
    
    def is_overdue(self):
        return timezone.now() > self.deadline