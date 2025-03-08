# Generated by Django 5.1.6 on 2025-03-08 13:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0005_alter_doctorsprofileinfo_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorsprofileinfo',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
