# Generated by Django 4.2 on 2023-05-19 00:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinica_app', '0022_rename_doctoravailability_slot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctoravailability_set', to='clinica_app.doctor'),
        ),
    ]
# Generated by Django 4.2 on 2023-05-19 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinica_app', '0022_rename_doctoravailability_slot_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctoravailability_set', to='clinica_app.doctor'),
        ),
    ]
