import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)
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

    def __str__(self):
        return f"Parcel {self.pk} {self.sender} - {self.recipient.username}"


@receiver(post_save, sender=Parcel)
def update_status(sender, instance, **kwargs):
    # print(sender, instance, instance.status)
    if instance is not None and instance.post_machine_locker is not None:
        if instance.status:
            parcel_locker = Locker.objects.get(pk=instance.post_machine_locker.pk)
            if not parcel_locker.status:
                parcel_locker.status = instance.status
                parcel_locker.save()
                print(f"Parcel {instance} is loaded into the Locker {parcel_locker.pk} {instance.status}")

