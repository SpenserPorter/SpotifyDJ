# Generated by Django 2.0.8 on 2018-09-30 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180930_1732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='playlists', to='api.Party'),
        ),
        migrations.AlterField(
            model_name='song',
            name='playlists',
            field=models.ManyToManyField(related_name='songs', to='api.Playlist'),
        ),
    ]