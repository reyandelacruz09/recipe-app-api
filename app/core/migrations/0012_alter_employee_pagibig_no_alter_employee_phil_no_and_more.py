# Generated by Django 4.0.10 on 2024-09-12 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_employee_pagibig_no_employee_phil_no_employee_sss_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='pagibig_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='phil_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='sss_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='tin_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
