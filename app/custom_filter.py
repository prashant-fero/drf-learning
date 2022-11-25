from django_filters import rest_framework as filters
from rest_framework import filters as filter
from app.models import Student


class StudentFilter(filters.FilterSet):
    class Meta:
        model = Student
        fields = ['name', 'dob']


class DynamicSearchFilter(filter.SearchFilter):

    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])
