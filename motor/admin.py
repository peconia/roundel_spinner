from django.contrib import admin
from motor.models import Job



class JobAdmin(admin.ModelAdmin):
    fields = ['action', 'status']
    list_display = ['action', 'status', 'created', 'last_modified', 'status_updated_time']
    list_filter = ['action', 'status', 'created', 'last_modified', 'status_updated_time']

admin.site.register(Job, JobAdmin)
