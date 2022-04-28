""" serializers class """
from datetime import date
from enum import unique
from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator

from .models import Student, Course, Movie, Album, Track, Resource, ModelA


class StudentSerializer(serializers.ModelSerializer):
    """student serializer"""

    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Student.objects.all())]
    )

    def validate(self, attrs):
        """custom validation"""
        if attrs.get("dob") >= date.today():
            raise serializers.ValidationError(
                {"dob": "Please enter valid date of birth"}
            )

        if len(attrs.get("name")) < 4:
            raise serializers.ValidationError(
                {"name": "Please enter at least 3 char name"}
            )

        return super().validate(attrs)

    class Meta:
        """meta info"""

        model = Student
        fields = ["id", "name", "dob", "age"]


class CourseSerializer(serializers.ModelSerializer):
    """course serializer"""

    # student = StudentSerializer(read_only=True)

    class Meta:
        """meta info"""

        model = Course
        fields = "__all__"
        depth = 1


class UserSerializer(serializers.Serializer):
    """user serializer"""

    def check_lenght(value):
        if len(value) < 3:
            raise serializers.ValidationError("at least 3 char in username")

    # id = serializers.SerializerMethodField( )
    username = serializers.CharField(validators=[check_lenght])
    password = serializers.CharField(write_only=True)

    # def get_id(self, obj):
    #     print(obj)
    #     return obj.id

    def create(self, validated_data):
        """create user"""
        self.check_unique_username(validated_data.get("username"))
        return User.objects.create(**validated_data)

    def check_unique_username(self, username, id=None):
        """check unique username"""
        user_obj = User.objects.filter(username=username)
        if id:
            user_obj = user_obj.exclude(id=id)
        if user_obj.exists():
            raise serializers.ValidationError({"username": "Username already exist"})

    def update(self, instance, validated_data):
        """update method"""
        self.check_unique_username(validated_data.get("username"), instance.id)
        instance.username = validated_data.get("username")
        instance.set_password(validated_data.get("password"))
        return instance

    def to_representation(self, instance):
        """pass extra data"""
        data = super().to_representation(instance)
        data.update(id=instance.id)
        return data

    def save(self):
        """save method"""
        print("validate data ", self.validated_data)
        print("context data ", self.context)
        return super().save()

    class Meta:
        """meta info"""

        fields = ["username"]


class MovieSerializer(serializers.ModelSerializer):  # create class to serializer model
    """movie serializer"""

    # creator = serializers.ReadOnlyField(source="creator.username")
    creator = serializers.StringRelatedField()

    class Meta:
        """model meta info"""

        model = Movie
        fields = ("id", "title", "genre", "year", "creator")


class UserModelSerializer(
    serializers.ModelSerializer
):  # create class to serializer user model
    """user model serializer"""

    # movies = serializers.PrimaryKeyRelatedField(many=True, queryset=Movie.objects.all())
    # movies = MovieSerializer(many=True)
    movies = serializers.StringRelatedField(many=True)
    # movies = serializers.SlugRelatedField(slug_field='title', queryset = Movie.objects.all())

    class Meta:
        """model meta info"""

        model = User
        fields = ("id", "username", "movies")


class AlbumSerializer(serializers.ModelSerializer):
    tracks = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = ["album_name", "artist", "tracks"]


class TrackSerializer(serializers.ModelSerializer):
    # album = serializers.StringRelatedField()
    # album = serializers.PrimaryKeyRelatedField(read_only=True)
    album = serializers.SlugRelatedField(
        slug_field="album_name", queryset=Album.objects.all()
    )

    class Meta:
        model = Track
        fields = ["album", "order", "duration", "title"]


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["likes"] = instance.liked_by.count()

        return representation

    def to_internal_value(self, data):
        print(data)
        return super().to_internal_value(data)


class ModelASerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelA
        fields = "__all__"
        depth = 2
