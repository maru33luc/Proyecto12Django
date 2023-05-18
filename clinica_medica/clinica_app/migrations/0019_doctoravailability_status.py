# Generated by Django 4.1.3 on 2023-05-17 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinica_app', '0018_remove_appointment_doctor_availability_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctoravailability',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('booked', 'Booked')], default='available', max_length=10),
        ),
    ]
