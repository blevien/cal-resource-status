# Generated by Django 4.2.3 on 2023-07-30 02:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_remove_event_location_event_locations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='display',
            name='calendars',
        ),
        migrations.AddField(
            model_name='display',
            name='calendar',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='schedule.calendar'),
        ),
    ]
