from django.contrib.auth.models import User
from django.utils import timezone

from django.test import TestCase, Client
from parcel import models as parcel_models
from post_machine import models as post_machine_models
class TestCasesUser(TestCase):
    fixtures = ['data']

    def setUp(self):
        test_post_machine = post_machine_models.PostMachine.objects.get(pk=1)
        test_locker = post_machine_models.Locker.objects.filter(post_machine=test_post_machine).all()[0]
        self.test_parcel = parcel_models.Parcel(
            recipient=User.objects.create_user(username='test_user', password='test_password'),
            sender='Michael Jackson',
            size=3,
            post_machine_recipient=test_post_machine,
            post_machine_locker=test_locker,
            send_date_time=timezone.now(),
            open_date_time=timezone.now(),
            status=False
        )
        self.test_parcel.save()
        self.test_parcel.post_machine_locker.status = True
        self.test_parcel.post_machine_locker.save()

    def test_get_parcel(self):
        actual_locker = post_machine_models.Locker.objects.get(pk=self.test_parcel.post_machine_locker.pk)
        self.assertEqual(actual_locker.status, True)
        c = Client()
        c.login(username='admin', password='admin')
        response = c.post(f'/user/parcels/{self.test_parcel.pk}/get_parcel/')
        self.assertEqual(response.status_code, 302)
        actual_parcel = parcel_models.Parcel.objects.get(pk=self.test_parcel.pk)
        self.assertEqual(actual_parcel.status, True)
        actual_locker = post_machine_models.Locker.objects.get(pk=self.test_parcel.post_machine_locker.pk)
        self.assertEqual(actual_locker.status, False)
