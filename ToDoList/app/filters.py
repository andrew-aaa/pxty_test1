import django_filters
from .models import Task

class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'priority': ['exact'],
            'status': ['exact'],
            'due_date': ['lt', 'gt'],  # Фильтр по дате (меньше/больше)
        }