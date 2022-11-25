"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.urls import path, include

from app.models import ModelA

from .views import (
    student_view,
    student_detail_view,
    CourseView,
    CourseUpdateView,
    UserListView,
    UserUpdateView,
    UserListApiView,
    AlbumListView,
    MoviesListView,
    TrackListView,
    ExampleView,
    HelloView,
    ResourceListView,
    ModelAListView,
    ModelAViewSet,
    StudentViewSet,
    ItemViewSet,
    TicketViewSet,
    StudentDataViewSet,
    home
)
from rest_framework.routers import DefaultRouter, SimpleRouter

router = SimpleRouter()
router.register("model", ModelAViewSet)
# router.register("student-data", StudentViewSet)
router.register("item_data", ItemViewSet)
router.register("ticket", TicketViewSet)
router.register("student-data", StudentDataViewSet)

urlpatterns = [
    path("api/", include(router.urls)),
    path("home/", home),
    path("student/", student_view, name="student_list"),
    path("student/<int:pk>/", student_detail_view, name="student_detail"),
    # Apiview
    path("course/", CourseView.as_view(), name="course_list"),
    path("course/<int:pk>", CourseUpdateView.as_view(), name="course_update"),
    path("user/", UserListView.as_view(), name="user_list_view"),
    path("users", UserListApiView.as_view(), name="user_list_view"),
    path("user/<int:pk>", UserUpdateView.as_view(), name="user_update_view"),
    path("album/", AlbumListView.as_view(), name="album"),
    path("movies/", MoviesListView.as_view(), name="movies"),
    path("tracks/", TrackListView.as_view(), name="tracks"),
    path("example/", ExampleView.as_view(), name="example"),
    path("hello/", HelloView.as_view(), name="hello"),
    path("resource/", ResourceListView.as_view(), name="resource"),
    path("modela/", ModelAListView.as_view(), name="model_a"),
    path("", include(router.urls)),
]
