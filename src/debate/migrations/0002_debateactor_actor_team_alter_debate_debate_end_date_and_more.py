# Generated by Django 4.0.7 on 2022-08-18 14:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='debateactor',
            name='actor_team',
            field=models.CharField(default='a', max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='debate',
            name='debate_end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 19, 20, 13, 33, 227834)),
        ),
        migrations.AlterField(
            model_name='debate',
            name='debate_start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 19, 17, 13, 33, 227834)),
        ),
    ]