from rest_framework import generics, permissions, filters
from .models import Todo, Task
from .serializers import TodoSerializer, UserSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.http import HttpResponse
import csv
from django.utils import timezone
from datetime import datetime
from django.core.exceptions import PermissionDenied
import json
from django.db.models import Q
from asgiref.sync import sync_to_async
import asyncio
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import TaskForm, TaskFilterForm
from .filters import TaskFilter


class TodoListCreate(generics.ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'deadline']

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TodoRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class ExportTodos(APIView):
    permission_classes = [IsAuthenticated]

    async def get(self, request):
        # Фильтрация задач текущего пользователя
        todos = await sync_to_async(list)(Todo.objects.filter(owner=request.user))
        
        # Создаем CSV в памяти
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="todos_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'Title', 'Description', 'Created At', 
                        'Deadline', 'Priority', 'Status'])
        
        for todo in todos:
            writer.writerow([
                todo.id,
                todo.title,
                todo.description,
                todo.created_at.strftime('%Y-%m-%d %H:%M'),
                todo.deadline.strftime('%Y-%m-%d %H:%M') if todo.deadline else '',
                todo.get_priority_display(),
                todo.get_status_display(),
            ])
        
        return response


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('task_list')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created')
    
    # Фильтрация
    filter_form = TaskFilterForm(request.GET)
    if filter_form.is_valid():
        if filter_form.cleaned_data['status']:
            tasks = tasks.filter(status=filter_form.cleaned_data['status'])
        if filter_form.cleaned_data['priority']:
            tasks = tasks.filter(priority=filter_form.cleaned_data['priority'])
    
    context = {
        'tasks': tasks,
        'filter_form': filter_form,
    }
    return render(request, 'todos/task_list.html', context)

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    
    # Сохраняем параметры фильтра в URL возврата
    back_url = 'task_list'
    if request.GET:
        back_url = f"{back_url}?{request.GET.urlencode()}"
    
    return render(request, 'todos/task_form.html', {
        'form': form,
        'back_url': back_url
    })

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    
    # Сохраняем параметры фильтра
    back_url = 'task_list'
    if request.GET:
        back_url = f"{back_url}?{request.GET.urlencode()}"
    
    return render(request, 'todos/task_form.html', {
        'form': form,
        'back_url': back_url
    })

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'todos/task_confirm_delete.html', {'task': task})