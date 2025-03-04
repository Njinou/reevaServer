from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Project, Task

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'status', 'deadline', 'created_at')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'project', 'assignee', 'status', 'priority', 'due_date')
