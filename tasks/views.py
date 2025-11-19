from django.shortcuts import render, get_object_or_404
from django import forms
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.urls import reverse
from .models import Task
from django.views.decorators.csrf import csrf_exempt
import json

# Form class for adding a new task
class NewTaskForm(forms.Form):
    task = forms.CharField(
        label='New task:',  
        widget=forms.TextInput(attrs={
            'autofocus': 'autofocus', 
            'id': 'task', 
            'placeholder': 'New Task'
        })
    )
    description = forms.CharField(
        label='Description',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Optional description',
            'rows': 7
        })
    )
    due_date = forms.DateField(
        label='Due date of task',
        widget=forms.DateInput(attrs={
            'type': 'date',  # This ensures a date picker is shown in modern browsers
            'placeholder': 'YYYY-MM-DD',
            'class': 'datepicker',  # You can add CSS classes if needed
        })
     )
    completed = forms.BooleanField(required=False)

# Index View - Home page showing task list
def index(request):
    # Fetch all tasks from the database to display them
    tasks = Task.objects.all()
    return render(request, "tasks/index.html", {
        "tasks": tasks  # Pass tasks to the template
    })

# Modify View - Page to modify existing tasks
def modify(request):
    tasks = Task.objects.all()  # Fetch all tasks from the database
    return render(request, "tasks/modify.html", {
        "tasks": tasks  # Pass tasks to the template
    })

# Add View - Adding a new task via form
def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task_name = form.cleaned_data["task"]
            description = form.cleaned_data["description"]
            due_date = form.cleaned_data["due_date"]
            completed = form.cleaned_data["completed"]
            Task.objects.create(name=task_name, description=description, due_date=due_date, completed=completed)  # Create a new Task object and save it in the database
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {
                "form": form
            })
    return render(request, "tasks/add.html", {
        "form": NewTaskForm()
    })

# API View to Get a List of Tasks
def get_tasks(request):
    tasks = Task.objects.all().values("id", "name", "description", "due_date", "completed")  # Get all tasks from the database
    return JsonResponse(list(tasks), safe=False)  # Return tasks as JSON

# API View to Get a Specific Task
def get_task(request, id):
    task = get_object_or_404(Task, id=id)  # Fetch a specific task by ID or return a 404 if not found
    return JsonResponse({"id": task.id, "name": task.name, "description": task.description, "due_date": task.due_date.strftime('%Y-%m-%d') if task.due_date else None, "completed": task.completed})
    # Date formatted as 'YYYY-MM-DD' or None if no due date

# API View to Create a New Task
@csrf_exempt  # To allow POST requests without CSRF protection for the sake of API
def create_task(request):
    if request.method == "POST":
        data = json.loads(request.body)  # Parse incoming JSON data
        task_name = data.get("task")
        if task_name:
            task = Task.objects.create(name=task_name)  # Create and save the new task in the database
            return JsonResponse({"message": "Task added successfully", "task": {"id": task.id, "name": task.name}}, status=201)
        else:
            return JsonResponse({"error": "Task content not provided."}, status=400)
    return HttpResponseNotAllowed(["POST"])

# API View to Update a Task
@csrf_exempt
def update_task(request, id):
    if request.method in ["PUT", "PATCH"]:
        task = get_object_or_404(Task, id=id)  # Fetch the task by ID or return a 404 if not found
        data = json.loads(request.body)
        task_name = data.get("name", task.name)  # Default to existing name if not provided
        completed = data.get("completed", task.completed)  # Default to existing completed status if not provided
        
        # Update task fields with provided data or keep existing values
        task.name = data.get("name", task.name)
        task.description = data.get("description", task.description)
        task.due_date = data.get("due_date", task.due_date)
        task.completed = data.get("completed", task.completed)

        task.save()  # Save the updated task to the database
        return JsonResponse({"message": "Task updated successfully", "task": {"id": task.id, "name": task.name, "completed": task.completed}})
    return HttpResponseNotAllowed(["PUT", "PATCH"])

# API View to Delete a Task
@csrf_exempt
def delete_task(request, id):
    if request.method == "DELETE":
        task = get_object_or_404(Task, id=id)  # Fetch the task by ID or return a 404 if not found
        task.delete()  # Delete the task from the database
        return JsonResponse({"message": "Task deleted successfully."})
    return HttpResponseNotAllowed(["DELETE"])
