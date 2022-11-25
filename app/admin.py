""" models register on admin panel """
from http.cookiejar import Cookie
from django.contrib import admin

from .models import (
    Student,
    Course,
    Movie,
    Album,
    Track,
    Resource,
    ModelA,
    ModelB,
    ModelC,
    Item,
    StudentData
)

# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Movie)
admin.site.register(Album)
admin.site.register(Track)
admin.site.register(Resource)
admin.site.register(ModelA)
admin.site.register(ModelB)
admin.site.register(ModelC)
admin.site.register(Item)
admin.site.register(StudentData)
