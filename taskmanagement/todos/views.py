from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Task

# Authentication Views
class SignupView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('task_list')
        return render(request, 'todos/signup.html')
    
    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Validation
        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, 'todos/signup.html')
        
        if password != password_confirm:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'todos/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return render(request, 'todos/signup.html')
        
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, f'Welcome {username}! Your account has been created.')
        return redirect('task_list')

class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('task_list')
        return render(request, 'todos/login.html')
    
    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid username or password.')
            return render(request, 'todos/login.html')

class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
        return redirect('login')

# Task Views
class TaskListView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        tasks = Task.objects.filter(user=request.user)
        return render(request, 'todos/task_list.html', {'tasks': tasks})

class TaskCreateView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request):
        return render(request, 'todos/task_form.html')
    
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        
        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description
            )
            messages.success(request, 'Task created successfully!')
        
        return redirect('task_list')

class TaskUpdateView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        return render(request, 'todos/task_form.html', {'task': task})
    
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.title = request.POST.get('title')
        task.description = request.POST.get('description', '')
        task.save()
        messages.success(request, 'Task updated successfully!')
        return redirect('task_list')

class TaskDeleteView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')

class TaskToggleView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.completed = not task.completed
        task.save()
        return redirect('task_list')
