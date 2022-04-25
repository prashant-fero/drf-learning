""" view files """
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer

from .serializers import StudentSerializer
from .models import Student

# Create your views here.
@api_view(['GET' , 'POST'])
def student_view(request):
    if request.method == "GET":
        student_obj = Student.objects.all()
        student_data = StudentSerializer(student_obj, many=True)
        return Response(student_data.data)
    elif request.method == "POST":
        student_obj = StudentSerializer(data=request.data)
        if student_obj.is_valid():
            student_obj.save()
            return Response(student_obj.data)
        return Response(student_obj.errors)