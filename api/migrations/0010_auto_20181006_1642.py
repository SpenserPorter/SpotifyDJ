# Generated by Django 2.0.8 on 2018-10-06 16:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_songvotes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='added_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='songs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='songvotes',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='voted_songs', to=settings.AUTH_USER_MODEL),
        ),
    ]
