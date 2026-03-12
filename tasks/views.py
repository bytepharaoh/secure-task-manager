from django.contrib.auth.decorators import login_required
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .models import Task
from .forms import TaskForm


def _get_user_task_or_404(user, pk):
    return get_object_or_404(Task, pk=pk, user=user)


def index(request):
    if request.user.is_authenticated:
        tasks = (
            Task.objects.filter(user=request.user)
            .annotate(
                priority_rank=Case(
                    When(priority="high", then=Value(3)),
                    When(priority="medium", then=Value(2)),
                    When(priority="low", then=Value(1)),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            .order_by("completed", "-priority_rank", "due_date", "-created_at")
        )
    else:
        tasks = []

    context = {
        'app_name': 'Secure Task Manager',
        'tasks': tasks
    }
    return render(request, 'tasks/index.html', context)


@login_required
@require_POST
def create_task(request):
    form = TaskForm(request.POST)
    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()
        return redirect('home')
    return render(request, 'tasks/create.html' , {'form':form})


@login_required
def create_task_form(request):
    form = TaskForm()
    return render(request, 'tasks/create.html' , {'form':form})


@login_required
def edit_task(request , pk):
    task = _get_user_task_or_404(request.user, pk)
    if request.method == 'POST':
        form = TaskForm(request.POST , instance=task)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TaskForm(instance=task)
    return render (request , 'tasks/edit.html' , {'form':form , 'task':task})


@login_required
@require_POST
def delete_task(request , pk):
    task = _get_user_task_or_404(request.user, pk)
    task.delete()
    return redirect('home')


@login_required
@require_POST
def toggle_complete(request , pk):
    task = _get_user_task_or_404(request.user, pk)
    task.completed = not task.completed
    task.save()
    return redirect('home')
