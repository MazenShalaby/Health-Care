# Generated by Django 5.1.6 on 2025-03-08 23:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customize', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='previoushistory',
            name='images',
        ),
        migrations.AddField(
            model_name='previoushistory',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='previous_history/'),
        ),
        migrations.AlterField(
            model_name='previoushistory',
            name='receiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='previoushistory',
            name='sender',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
