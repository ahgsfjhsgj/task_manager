from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .forms import TaskForm
from .models import Task
from django.db.models import Q
from myapp.models import UserProfile



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'login.html')



def task_list(request):
    tasks = Task.objects.all()
    search_query = request.GET.get('search', '')
    
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    context = {
        'tasks': tasks,
        'search_query': search_query,
        'pending_count': Task.objects.filter(status='PENDING').count(),
        'overdue_count': Task.objects.filter(status='OVERDUE').count(),
        'completed_count': Task.objects.filter(status='COMPLETED').count(),
    }
    return render(request, 'myapp/task_list.html', context)

def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task created successfully!')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'myapp/task_form.html', {'form': form, 'title': 'Create Task'})

def task_update(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'myapp/task_form.html', {'form': form, 'title': 'Update Task'})

def task_delete(request, id):
    task = get_object_or_404(Task, id=id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('task_list')
    return render(request, 'myapp/task_confirm_delete.html', {'task': task})

def analytics_view(request):
    total_tasks = Task.objects.count()
    completed_count = Task.objects.filter(status='COMPLETED').count()
    pending_count = Task.objects.filter(status='PENDING').count()
    in_progress_count = Task.objects.filter(status='IN_PROGRESS').count()
    overdue_count = Task.objects.filter(status='OVERDUE').count()
    
    completion_rate = (completed_count / total_tasks * 100) if total_tasks > 0 else 0
    
    # Calculate percentages for bars
    total = total_tasks or 1  # Avoid division by zero
    pending_percentage = (pending_count / total) * 100
    in_progress_percentage = (in_progress_count / total) * 100
    completed_percentage = (completed_count / total) * 100
    
    context = {
        'total_tasks': total_tasks,
        'completion_rate': round(completion_rate, 1),
        'overdue_count': overdue_count,
        'pending_count': pending_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'pending_percentage': pending_percentage,
        'in_progress_percentage': in_progress_percentage,
        'completed_percentage': completed_percentage,
        'status_bars': [
            {'label': 'Pending', 'percentage': pending_percentage, 'count': pending_count},
            {'label': 'In Progress', 'percentage': in_progress_percentage, 'count': in_progress_count},
            {'label': 'Completed', 'percentage': completed_percentage, 'count': completed_count},
        ],
    }
    return render(request, 'myapp/analytics.html', context)

@login_required
def settings_view(request):
    # Create profile if it doesn't exist
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        profile.default_view = request.POST.get('default_view', 'all')
        profile.enable_reminders = 'enable_reminders' in request.POST
        profile.theme = request.POST.get('theme', 'light')
        profile.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('settings')
    
    context = {
        'default_view': profile.default_view,
        'enable_reminders': profile.enable_reminders,
        'theme': profile.theme,
    }
    return render(request, 'myapp/settings.html', context)

def task_detail(request, id):
    task = get_object_or_404(Task, id=id)
    
    if request.method == 'POST' and 'mark_complete' in request.POST:
        task.status = 'COMPLETED'
        task.save()
        messages.success(request, 'Task marked as complete!')
        return redirect('task_detail', id=id)
    
    context = {
        'task': task,
        'pending_count': Task.objects.filter(status='PENDING').count(),
        'overdue_count': Task.objects.filter(status='OVERDUE').count(),
        'completed_count': Task.objects.filter(status='COMPLETED').count(),
    }
    return render(request, 'myapp/task_detail.html', context)