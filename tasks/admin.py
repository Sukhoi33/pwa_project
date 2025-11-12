from django.contrib import admin
from .models import Task
#admin.site.register(Task)


# Create a custom admin class for Task so you can see the created_at field and other other features in admin
class TaskAdmin(admin.ModelAdmin):
    # Add the 'created_at' field to the list display
    list_display = ('name', 'description', 'completed', 'due_date', 'created_at', 'updated_at')
    
    # Make 'created_at' read-only in the form view (but visible)
    readonly_fields = ('created_at',)
    
    # Optionally, you can add a filter by 'completed' status and search by 'name'
    list_filter = ('completed',)
    search_fields = ('name',)
    
    # Optionally, you can use date_hierarchy for easier date-based navigation
    date_hierarchy = 'created_at'
    
    # Ordering the list by 'created_at', so newest tasks show up first
    ordering = ('-created_at',)

# Register the Task model with the custom TaskAdmin
admin.site.register(Task, TaskAdmin)
