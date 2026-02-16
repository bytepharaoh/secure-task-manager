from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required 
from .models import Task
from .forms import TaskForm

def index(request):
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        tasks = sorted(tasks, key=lambda t: (
            t.completed,                           # False (0) comes before True (1)
            -t.priority_order(),                   # Negative for descending (high first)
           # t.due_date if t.due_date else '9999-12-31'  # Tasks without due dates go last
        ))

    else:
        tasks = []  # Empty list for logged-out users
    
    context = {
        'app_name': 'Secure Task Manager',
        'tasks': tasks
    }
    return render(request, 'tasks/index.html', context)
@login_required 

def create_task(request):
    if request.method=='POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task= form.save(commit=False)
            task.user=request.user
            task.save()
            return redirect('home')
    else:
        form = TaskForm()
    return render(request, 'tasks/create.html' , {'form':form})
@login_required 
def edit_task(request , pk):
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST , instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render (request , 'tasks/edit.html' , {'form':form , 'task':task})
@login_required
def delete_task(request , pk):
    task = Task.objects.get(pk=pk)
    task.delete()
    return redirect('home')
@login_required
def toggle_complete(request , pk):
    task= Task.objects.get(pk=pk)
    task.completed = not task.completed
    task.save()
    return redirect('home')
# Create your views here.
