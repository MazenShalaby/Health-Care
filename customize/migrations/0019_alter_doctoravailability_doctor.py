# Generated by Django 5.1.6 on 2025-03-08 14:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0018_alter_doctoravailability_doctor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctoravailability',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customize.doctorsprofileinfo'),
        ),
    ]
