""" serializers class """
from datetime import date
from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Student, Course


class StudentSerializer(serializers.ModelSerializer):
    """student serializer"""

    def validate(self, attrs):
        """custom validation"""
        if attrs.get("dob") >= date.today():
            raise serializers.ValidationError(
                {"dob": "Please enter valid date of birth"}
            )
        return super().validate(attrs)

    class Meta:
        """meta info"""

        model = Student
        fields = ["id", "name", "dob", "age"]


class CourseSerializer(serializers.ModelSerializer):
    """ course serializer """

    student = StudentSerializer(read_only=True)

    class Meta:
        """meta info"""

        model = Course
        fields = "__all__"


class UserSerializer(serializers.Serializer):
    """ user serializer"""

    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def create(self, validated_data):
        """ create user """
        return User.objects.create(**validated_data)

    class Meta:
        """meta info"""

        fields = ["username"]
