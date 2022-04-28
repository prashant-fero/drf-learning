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

    def __str__(self) -> str:
        return self.title


class Album(models.Model):
    """album"""

    album_name = models.CharField(max_length=100)
    artist = models.CharField(max_length=100)


class Track(models.Model):
    """track"""

    album = models.ForeignKey(Album, related_name="tracks", on_delete=models.CASCADE)
    order = models.IntegerField()
    title = models.CharField(max_length=100)
    duration = models.IntegerField()

    class Meta:
        unique_together = ["album", "order"]
        ordering = ["order"]

    def __str__(self):
        return "%d: %s" % (self.order, self.title)


class Resource(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    liked_by = models.ManyToManyField(to="auth.User")

    def __str__(self):
        return f"{self.title}"


class ModelC(models.Model):
    content = models.CharField(max_length=128)


class ModelB(models.Model):
    model_c = models.ForeignKey(to=ModelC, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)


class ModelA(models.Model):
    model_b = models.ForeignKey(to=ModelB, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
