from django.contrib import admin
from .models import Job

# register Job model to interact with the model via Django admin interface
admin.site.register(Job)

# COMMANDS:
# python manage.py makemigrations (generate SQL commands to create database schema)
# python manage.py migrate (apply them to database)