# Generated by Django 4.0.10 on 2024-08-31 06:49

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_newsfile_date_uploaded_newsfile_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='date_uploaded',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
