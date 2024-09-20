

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('first_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('username', models.CharField(blank=True, max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_url', models.URLField(blank=True, null=True)),
                ('logo', models.ImageField(blank=True, default=None, null=True, upload_to='client_logo')),
                ('address_1', models.TextField(blank=True, null=True)),
                ('address_2', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=50, null=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (4, 'Suspended'), (5, 'Deleted'), (2, 'Incomplete Profile'), (3, 'For Activation')], default=1)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_created_by', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('info', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('representative', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Department',
                'verbose_name_plural': 'Department',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('control_number', models.CharField(blank=True, max_length=255, null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive'), (3, 'Incomplete'), (4, 'Deleted')], default=1)),
                ('access_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='form_access_type', to='core.department')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='form_client', to='core.client')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='form_department', to='core.department')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Document',
                'verbose_name_plural': 'Documents',
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('is_seen', models.BooleanField(default=False)),
                ('file', models.FileField(blank=True, null=True, upload_to='notification')),
                ('message', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('from_client', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notif_from_client', to='core.client')),
                ('receiver', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notif_receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notif_sender', to=settings.AUTH_USER_MODEL)),
                ('to_client', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notif_to_client', to='core.client')),
            ],
            options={
                'verbose_name': 'Notification',
                'verbose_name_plural': 'Notifications',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('memo_number', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('start', models.DateField(blank=True, null=True)),
                ('end', models.DateField(blank=True, null=True)),
                ('ftp', models.FileField(blank=True, null=True, upload_to='memo')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('text', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (2, 'Inactive'), (3, 'Incomplete'), (4, 'Deleted')], default=1)),
                ('access_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='memo_access_type', to='core.department')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='memo_client', to='core.client')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='memo_department', to='core.department')),
                ('uploaded_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(blank=True, default=None, null=True, upload_to='profile')),
                ('employee_id', models.CharField(blank=True, max_length=255, null=True)),
                ('gender', models.IntegerField(choices=[(1, 'male'), (2, 'female')])),
                ('date_hired', models.DateField(blank=True, null=True)),
                ('job_title', models.CharField(max_length=255)),
                ('address_1', models.TextField(blank=True, null=True)),
                ('address_2', models.TextField(blank=True, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('mobile_number', models.CharField(blank=True, max_length=50, null=True)),
                ('martial_status', models.IntegerField(choices=[(1, 'Single'), (2, 'Married')])),
                ('birthday', models.DateField(blank=True, null=True)),
                ('employee_status', models.IntegerField(choices=[(1, 'Probationary'), (2, 'Project'), (3, 'Regular')])),
                ('user_type', models.IntegerField(choices=[(1, 'Super Admin'), (2, 'Admin'), (3, 'Standard')], default=3)),
                ('office_location', models.CharField(blank=True, max_length=50, null=True)),
                ('work_arrangement', models.IntegerField(choices=[(1, 'Probationary'), (2, 'Project'), (3, 'Regular')])),
                ('course_to_do', models.IntegerField(default=0)),
                ('overdue_course', models.IntegerField(default=0)),
                ('completed_course', models.IntegerField(default=0)),
                ('contact_person_incase_of_emergency', models.CharField(max_length=255)),
                ('cpioe_contact_no', models.CharField(max_length=255)),
                ('status', models.IntegerField(choices=[(1, 'Active'), (4, 'Suspended'), (5, 'Deleted'), (2, 'Incomplete Profile'), (3, 'For Activation')], default=1)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', to='core.client')),
                ('department', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.department')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='client_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
        migrations.CreateModel(
            name='DocumentFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ftp', models.FileField(blank=True, null=True, upload_to='form')),
                ('link', models.URLField(blank=True, null=True)),
                ('date_uploaded', models.DateTimeField(auto_now_add=True)),
                ('version', models.CharField(blank=True, max_length=255, null=True)),
                ('document', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.document')),
            ],
            options={
                'verbose_name': 'Document Files',
                'verbose_name_plural': 'Document Files',
            },
        ),
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approve', models.BooleanField(default=False)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='attendance')),
                ('task_image', models.ImageField(blank=True, default=None, null=True, upload_to='attendance')),
                ('remarks', models.TextField(blank=True, null=True)),
                ('site_location', models.IntegerField(blank=True, choices=[(1, 'WFH'), (2, 'ON_SITE')], null=True)),
                ('type', models.IntegerField(blank=True, choices=[(1, 'TIMEIN'), (2, 'TIMEOUT'), (3, 'LEAVE')], null=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.employee')),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Attendance',
                'verbose_name_plural': 'Attendance',
            },
        ),
    ]
