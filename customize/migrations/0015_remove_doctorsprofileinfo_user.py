# Generated by Django 5.1.6 on 2025-03-08 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0014_alter_doctoravailability_doctor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctorsprofileinfo',
            name='user',
        ),
    ]
