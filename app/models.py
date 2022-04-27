""" model file """
from datetime import date
from django.db import models

# Create your models here.


class Student(models.Model):
    """student models"""

    name = models.CharField(max_length=50)
    dob = models.DateField()

    def __str__(self):
        """return string"""
        return f"{self.name}"

    @property
    def age(self):
        """calculate age"""
        return date.today().year - self.dob.year


class Course(models.Model):
    """course model"""

    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    student = models.ForeignKey(
        Student, related_name="votes", on_delete=models.CASCADE, default=1
    )

    def __str__(self) -> str:
        """return string"""
        return self.name


class Movie(models.Model):
    """movie model"""

    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    year = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(
        "auth.User", related_name="movies", on_delete=models.CASCADE
    )

    class Meta:
        """meta info"""

        ordering = ["-id"]
