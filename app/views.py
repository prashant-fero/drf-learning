""" view files """
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from app.tasks import add
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework import pagination
from rest_framework import viewsets
from rest_framework.decorators import action


# custom
from .serializers import (
    ModelASerializer,
    StudentSerializer,
    CourseSerializer,
    UserSerializer,
    MovieSerializer,
    UserModelSerializer,
    AlbumSerializer,
    MovieSerializer,
    TrackSerializer,
    ResourceSerializer,
)
from .models import ModelA, Student, Course, Movie, Album, Track, Resource

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
            print(student_obj.validated_data)
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

    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

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
    pagination_class = pagination.PageNumberPagination
    page_size = 2
    # page_size_query_param = 'page_size'
    # max_page_size = 50
    # page_query_param = 'p'


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


class UserListApiView(
    generics.ListAPIView,
):
    """user list api"""

    serializer_class = UserModelSerializer
    queryset = User.objects.all()


class AlbumListView(generics.ListAPIView):

    serializer_class = AlbumSerializer
    queryset = Album.objects.all()


class MoviesListView(generics.ListAPIView):

    serializer_class = MovieSerializer
    queryset = Movie.objects.all()


class TrackListView(generics.ListAPIView):

    serializer_class = TrackSerializer
    queryset = Track.objects.all()


class ExampleView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        content = {
            "user": str(request.user),  # `django.contrib.auth.User` instance.
            "auth": str(request.auth),  # None
        }
        return Response(content)


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)  # <-- And here

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


class ResourceListView(generics.ListCreateAPIView):

    serializer_class = ResourceSerializer
    queryset = Resource.objects.all()
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ["title"]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "liked_by__username"]


class ModelAListView(generics.ListAPIView):

    serializer_class = ModelASerializer
    queryset = ModelA.objects.all()


class ModelAViewSet(viewsets.ModelViewSet):

    serializer_class = ModelASerializer
    queryset = ModelA.objects.all()

    @action(
        methods=["post"],
        detail=True,
        url_path="change-password",
        url_name="change_password",
    )
    def custom_response(self, request, pk=None):
        return Response({"id": pk})

    @action(
        methods=["get"],
        detail=True,
        url_path="change-password",
        url_name="change_password",
    )
    def custom_response(self, request, pk=None):
        return Response({"id": pk})


def home(request):
    add.delay(3, 2)
    return JsonResponse({"request": "ok"})
