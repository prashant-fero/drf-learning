""" models register on admin panel """
from http.cookiejar import Cookie
from django.contrib import admin

from .models import Student, Course, Movie

# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Movie)
