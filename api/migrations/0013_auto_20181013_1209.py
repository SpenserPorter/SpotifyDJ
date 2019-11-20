# Generated by Django 2.0.8 on 2018-10-13 12:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0012_auto_20181006_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vote', models.BooleanField()),
                ('song', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voted', to='api.Song')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voted_songs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='songvote',
            name='song',
        ),
        migrations.RemoveField(
            model_name='songvote',
            name='user',
        ),
        migrations.DeleteModel(
            name='SongVote',
        ),
    ]