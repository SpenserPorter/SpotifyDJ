# Generated by Django 2.0.8 on 2018-10-06 17:10

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0010_auto_20181006_1642'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SongVotes',
            new_name='SongVote',
        ),
    ]
