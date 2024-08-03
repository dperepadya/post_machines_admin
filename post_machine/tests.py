
from django.test import TestCase, Client
from parcel import models as parcel_models
from post_machine import models as post_machine_models

class TestCasesParcel(TestCase):
    fixtures = ['data']

    def setUp(self):
        self.test_post_machine = post_machine_models.PostMachine(
            address='Yellow str. 12',
            city='San Francisco'
        )
        self.test_post_machine.save()

    def test_get_post_machine(self):
        c = Client()
        response = c.get(f'/post_machine/100000/')
        self.assertEqual(response.status_code, 404)
        response = c.get(f'/post_machine/{self.test_post_machine.pk}/')
        self.assertEqual(response.status_code, 200)
        # test instances
        actual_post_machine = post_machine_models.PostMachine.objects.get(pk=self.test_post_machine.pk)
        self.assertEqual(actual_post_machine, self.test_post_machine)
        # test specific parameters
        self.assertEqual(actual_post_machine.address, self.test_post_machine.address)
