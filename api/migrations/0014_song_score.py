# Generated by Django 2.0.8 on 2018-10-16 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20181013_1209'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
