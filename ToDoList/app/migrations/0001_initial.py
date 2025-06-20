# Generated by Django 5.2.2 on 2025-06-18 18:19

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Заголовок')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата создания')),
                ('deadline', models.DateTimeField(blank=True, null=True, verbose_name='Дедлайн')),
                ('priority', models.CharField(choices=[('low', 'Низкий'), ('medium', 'Средний'), ('high', 'Высокий')], default='medium', max_length=10, verbose_name='Приоритет')),
                ('status', models.CharField(choices=[('done', 'Выполнено'), ('not_done', 'Не выполнено')], default='not_done', max_length=10, verbose_name='Статус')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='todos', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'ordering': ['-created_at'],
            },
        ),
    ]
