""" view files """
from unittest import result
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.core.mail import send_mail
from django.utils.safestring import mark_safe
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from django.contrib.auth.models import User
from rest_framework import pagination
from rest_framework import viewsets
from rest_framework.decorators import action
from app.custom_filter import DynamicSearchFilter

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
    ItemSerializer,
    TicketSerializer,
    StudentDataSerializer
)
from .models import ModelA, Student, Course, Movie, Album, Ticket, Track, Resource, Item, StudentData


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


class UserListApiView(generics.ListAPIView):
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
    search_fields = ["title",
                     "liked_by__username"]


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


class StudentViewSet(viewsets.ModelViewSet):
    """ student all data list """

    serializer_class = UserSerializer
    queryset = User.objects.all()


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    queryset = Ticket.objects.all()


class StudentDataViewSet(viewsets.ModelViewSet):
    serializer_class = StudentDataSerializer
    queryset = StudentData.objects.all()
    filter_backends = (DynamicSearchFilter,)


def home(request):
    data = {
        "username": "Prashant",
        "password": "sadfsdf",
    }
    result = dict()
    result["parsed_data"] = '''
               <p>Dear {customer}, </p>
                <p>Congratulations ! Welcome to Sky Express . Please use the below credentials to sign in. </p>
                <p><span class="text-danger">Username:</span> {username}</p>
                <p><span class="text-danger">Password:</span> {password}</p>
                <p><span class="text-danger">Login Link:</span> <a href="https://www.skyexpressinternational.com/Login" style="text-decoration: none;">https://www.skyexpressinternational.com/Login</a></p>
                <p><b>Note:</b>You can reset your password once you login using the above credentials.</p>
                <p>If you face any issue, please click on the link or email us at support@skyexpress.ae with your account code.</p>
            '''.format(customer="Prashant", username="prashant", password="123pra123")

    return render(request, "email.html")
    # subject = 'Test Mail'
    # message = f'test mail'
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = ["bhaliyakishan80@gmail.com"]
    # result = send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    # print("email result ",result)
    # add.delay(3, 2)
    # return JsonResponse({"request": "ok"})
