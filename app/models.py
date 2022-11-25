""" model file """
from datetime import date
from trace import Trace
from django.db import models
from auditlog.registry import auditlog

# Create your models here.


class Student(models.Model):
    """student models"""

    name = models.CharField(max_length=50)
    dob = models.DateField()

    def __str__(self):
        """return string"""
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if self.pk:
            # If self.pk is not None then it's an update.
            cls = self.__class__

            old = cls.objects.get(pk=self.pk)
            print("old value ", cls._meta.get_fields())
            print("new value ", self._meta.get_fields())
            # This will get the current model state since super().save() isn't called yet.
            new = self  # This gets the newly instantiated Mode object with the new values.
            changed_fields = []
            for field in cls._meta.get_fields():
                field_name = field.name
                try:
                    if getattr(old, field_name) != getattr(new, field_name):
                        changed_fields.append(field_name)
                except Exception as ex:  # Catch field does not exist exception
                    pass
            kwargs['update_fields'] = changed_fields
        super().save(*args, **kwargs)

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

class Item(models.Model):
    """ item model """
    title = models.CharField(max_length=60)
    student = models.ForeignKey(Student, related_name="item_students", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title}"

class Ticket(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f"{self.title}"

class TicketAttached(models.Model):

    file = models.FileField()
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)


class StudentData(models.Model):
    name = models.CharField(max_length=100)
    dob = models.DateField()

    def __str__(self):
        return self.name




auditlog.register(Student)
auditlog.register(Course)
auditlog.register(ModelB)
auditlog.register(ModelC)
auditlog.register(ModelA)
auditlog.register(Resource)
auditlog.register(Album)
auditlog.register(Track)
auditlog.register(Movie)
# auditlog.register(Item)
