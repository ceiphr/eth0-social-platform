# Generated by Django 2.0.7 on 2018-08-09 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0011_auto_20180809_0220'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='commentDownvotes',
            new_name='downvotes',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='commentUpvotes',
            new_name='upvotes',
        ),
    ]
