""" models register on admin panel """
from django.contrib import admin

from .models import Student

# Register your models here.
admin.site.register(Student)