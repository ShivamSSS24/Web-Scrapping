from django.contrib import admin
from .models import Job, Task

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    pass

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass
