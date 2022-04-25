""" model file """
from django.db import models


# Create your models here.

class Student(models.Model):
    """ student models """

    name = models.CharField(max_length=50)
    dob = models.DateField()

    def __str__(self):
        """ return string """
        return f"{self.name}"
    
    