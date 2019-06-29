# Generated by Django 2.0.7 on 2018-08-07 18:58

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('database', '0003_auto_20180805_0232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='postedBy',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.RemoveField(
            model_name='post',
            name='votes',
        ),
        migrations.AddField(
            model_name='post',
            name='votes',
            field=models.ManyToManyField(related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]