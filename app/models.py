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

    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=5)
    student = models.ForeignKey(
        Student, related_name="votes", on_delete=models.CASCADE, default=1
    )

    def __str__(self) -> str:
        return self.name
