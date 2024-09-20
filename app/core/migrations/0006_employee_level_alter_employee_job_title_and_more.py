from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_newsfile_news_officelocation_level_jobtittle'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.level'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='job_title',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.jobtittle'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='office_location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.officelocation'),
        ),
    ]
