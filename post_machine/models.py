from django.db import models


# Create your models here.
class PostMachine(models.Model):
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


class Locker(models.Model):
    size = models.PositiveSmallIntegerField()
    post_machine = models.ForeignKey(PostMachine, on_delete=models.CASCADE, related_name='lockers')
    status = models.BooleanField(default=False)
