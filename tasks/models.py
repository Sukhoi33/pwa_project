from django.db import models
from django.utils import timezone
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, help_text="Enter the category name.")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="subcategories")
    def __str__(self):
        return self.name


# Task model.
class Task(models.Model):
    name = models.CharField(max_length=255, help_text="Enter the task name.")
    completed = models.BooleanField(default=False, help_text="Is the task completed?")
    description = models.TextField(blank=True, help_text="Enter the task description.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The time when the task was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The time when the task was last updated.")
    due_date = models.DateTimeField(default=None, null=True, blank=True, help_text="The date when the task is due.")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")

    def __str__(self):
        return f"{self.name} (Completed: {self.completed})"