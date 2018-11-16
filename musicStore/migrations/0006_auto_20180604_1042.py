# Generated by Django 2.0.3 on 2018-06-04 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicStore', '0005_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('videofile', models.FileField(null=True, upload_to='videos/', verbose_name='')),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='musicStore.Song')),
            ],
        ),
        migrations.DeleteModel(
            name='Video',
        ),
    ]
