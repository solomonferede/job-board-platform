from django.contrib import admin
from .models import Job, Category, JobType, Location

admin.site.register(Job)
admin.site.register(Category)
admin.site.register(JobType)
admin.site.register(Location)
