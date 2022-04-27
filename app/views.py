""" view files """
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from django.contrib.auth.models import User

# custom
from .serializers import (
    StudentSerializer,
    CourseSerializer,
    UserSerializer,
    MovieSerializer,
    UserModelSerializer,
)
from .models import Student, Course, Movie

# Create your views here.
@api_view(["GET", "POST"])
def student_view(request):
    """student record create & fetch all student record"""
    if request.method == "GET":
        student_obj = Student.objects.all()
        student_data = StudentSerializer(student_obj, many=True)
        return Response(student_data.data)
    else:
        print("data ", request.data)
        student_obj = StudentSerializer(
            data=request.data, many=isinstance(request.data, list)
        )
        if student_obj.is_valid(raise_exception=True):
            student_obj.save()
            return Response(student_obj.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def student_detail_view(request, pk):
    """student detail view"""
    try:
        student = Student.objects.get(pk=pk)
        print("query parameter ", request.parsers)
        print("content type ", request.content_type)

    except Student.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        student_data = StudentSerializer(student)
        return Response(student_data.data)

    elif request.method == "PUT":
        student_data = StudentSerializer(student, data=request.data)
        if student_data.is_valid():
            student_data.save()
            return Response(
                student_data.data,
            )
        return Response(student_data.errors)

    else:
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CourseView(APIView):
    """course view"""

    def get(self, request):
        """get all course"""
        course_obj = Course.objects.all()
        course_serializer = CourseSerializer(course_obj, many=True)
        return Response(course_serializer.data)

    def post(self, request):
        """create new course"""
        # Create an article from the above data
        course_serializer = CourseSerializer(
            data=request.data, many=isinstance(request.data, list)
        )
        if course_serializer.is_valid(raise_exception=True):
            course_serializer.save()
            return Response(course_serializer.data)
        return Response(course_serializer.data)


class CourseUpdateView(generics.UpdateAPIView):
    """update api view"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class UserListView(generics.ListCreateAPIView):
    """user list view"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateView(generics.UpdateAPIView):
    """user update view"""

    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListCreateMovieAPIView(generics.ListCreateAPIView):
    """create & list api view"""

    serializer_class = MovieSerializer
    queryset = Movie.objects.all()

    def perform_create(self, serializer):
        # Assign the user who created the movie
        serializer.save(creator=self.request.user)


class UserListApiView(generics.ListAPIView):
    """user list api"""

    serializer_class = UserModelSerializer
    queryset = User.objects.all()
