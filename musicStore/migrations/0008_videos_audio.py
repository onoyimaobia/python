# Generated by Django 2.0.3 on 2018-06-04 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicStore', '0007_remove_videos_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='videos',
            name='audio',
            field=models.FileField(blank=True, upload_to='audio', verbose_name=''),
        ),
    ]
