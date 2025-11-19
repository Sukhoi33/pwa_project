from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.urls import reverse
from .models import Task
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import NewTaskForm
from .models import Category

def index(request):
    categories = Category.objects.filter(parent=None).prefetch_related('subcategories', 'tasks')
    return render(request, "tasks/index.html", {"categories": categories})

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
            category = form.cleaned_data.get("category")  # Get the optional category
            Task.objects.create(name=task_name, category=category)  # Save the Task with category if provided
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "tasks/add.html", {"form": form})
    
    return render(request, "tasks/add.html", {"form": NewTaskForm()})

# API View to Get a List of Tasks
def get_tasks(_request):  # Renamed parameter to avoid unused warning
    tasks = Task.objects.all().values("id", "name", "description", "due_date", "completed")  # Get all tasks from the database
    return JsonResponse(list(tasks), safe=False)  # Return tasks as JSON

# API View to Get a Specific Task
def get_task(_request, id):  # Renamed parameter to avoid unused warning
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
        print(completed)  # Added to use completed
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
