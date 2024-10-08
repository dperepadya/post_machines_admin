# Generated by Django 5.0.7 on 2024-07-18 10:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcel', '0006_alter_parcel_open_date_time_and_more'),
        ('post_machine', '0002_alter_locker_post_machine'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='post_machine_locker',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lockers', to='post_machine.locker'),
        ),
    ]
