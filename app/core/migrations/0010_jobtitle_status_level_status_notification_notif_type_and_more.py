# Generated by Django 4.0.10 on 2024-09-12 06:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_rename_contact_person_incase_of_emergency_employee_cpioe'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobtitle',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive'), (3, 'Deleted')], default=1),
        ),
        migrations.AddField(
            model_name='level',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive'), (3, 'Deleted')], default=1),
        ),
        migrations.AddField(
            model_name='notification',
            name='notif_type',
            field=models.IntegerField(choices=[(1, 'Feedback'), (2, 'Upload Logo Feature'), (3, 'Notify Client')], default=1),
        ),
        migrations.AddField(
            model_name='officelocation',
            name='status',
            field=models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive'), (3, 'Deleted')], default=1),
        ),
        migrations.CreateModel(
            name='EducBackGround',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(blank=True, max_length=255, null=True)),
                ('date_graduated', models.DateTimeField(blank=True, default=None, null=True)),
                ('degree', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.TextField(blank=True, null=True)),
                ('educ_type', models.IntegerField(choices=[(1, 'Primary Education'), (2, 'Secondary Education'), (2, 'Tertiary Education')], default=1)),
                ('employee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.employee')),
            ],
        ),
    ]