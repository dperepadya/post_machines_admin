import logging

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from post_machine.models import PostMachine, Locker

logger = logging.getLogger(__name__)


class Parcel(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.CharField(max_length=100)
    size = models.PositiveSmallIntegerField()
    post_machine_recipient = models.ForeignKey(PostMachine, on_delete=models.CASCADE, default=None)
    post_machine_locker = models.ForeignKey(Locker, on_delete=models.DO_NOTHING, null=True, default=None, related_name='lockers')
    send_date_time = models.DateTimeField()
    open_date_time = models.DateTimeField(null=True, default=None)
    status = models.BooleanField(default=False)  # True - Delivered

    def __str__(self):
        status_str = ""
        if self.post_machine_recipient is not None:
            status_str = "delivered" if self.status else\
                "on the way" if self.post_machine_locker is None else "waiting"
        return f"Parcel {self.pk} {self.sender} - {self.recipient.username} {status_str}"


@receiver(post_save, sender=Parcel)
def update_status(sender, instance, **kwargs):
    # print(sender, instance, instance.status)
    if instance is not None and instance.post_machine_locker is not None:
        parcel_locker = Locker.objects.get(pk=instance.post_machine_locker.pk)
        if instance.status:  # the parcel was marked as delivered
            if parcel_locker.status:  # loaded
                # make the locker empty
                parcel_locker.status = False
                parcel_locker.save()
                print(f"Parcel {instance} was picked up from the Locker {parcel_locker.pk} {instance.status} /"
                      f" {parcel_locker.status}")
        else:  # the parcel was just loaded into a locker
            if not parcel_locker.status:  # empty
                # make the locker empty
                parcel_locker.status = True  # loaded
                parcel_locker.save()
            print(f"Parcel {instance} is loaded into the Locker {parcel_locker.pk} {instance.status} /"
                  f" {parcel_locker.status}")
