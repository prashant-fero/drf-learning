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

from django.urls import path
from .views import (
    student_view,
    student_detail_view,
    CourseView,
    CourseUpdateView,
    UserListView,
)

urlpatterns = [
    path("student/", student_view, name="student_list"),
    path("student/<int:pk>/", student_detail_view, name="student_detail"),
    # Apiview
    path("course/", CourseView.as_view(), name="course_list"),
    path("course/<int:pk>", CourseUpdateView.as_view(), name="course_update"),
    path("user/", UserListView.as_view(), name="user_list_view"),
]
