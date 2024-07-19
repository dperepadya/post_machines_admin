from django.contrib.auth.models import User
from django.db import models

import user
from post_machine.models import PostMachine, Locker


# Create your models here.
class Parcel(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    size = models.PositiveSmallIntegerField()
    # post_machine_recipient = models.ForeignKey(PostMachine, on_delete=models.CASCADE, default=None)
    post_machine_locker = models.ForeignKey(Locker, on_delete=models.CASCADE, null=True, default=None, related_name='lockers')
    send_date_time = models.DateTimeField()
    open_date_time = models.DateTimeField(null=True, default=None)
    status = models.BooleanField(default=False)

