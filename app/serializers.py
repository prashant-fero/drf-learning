""" serializers class """
from datetime import date
from rest_framework import serializers

from .models import Student

class StudentSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        if attrs.get("dob") >= date.today():
            raise serializers.ValidationError({"dob" : "Please enter valid date of birth "})
        return super().validate(attrs)
        
    class Meta:
        model = Student
        fields = "__all__"

