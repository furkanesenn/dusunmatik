# Generated by Django 4.0.7 on 2022-08-19 18:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('debate', '0015_alter_debate_debate_announce_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='debate',
            name='debate_announce_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 19, 20, 57, 3, 584189)),
        ),
        migrations.AlterField(
            model_name='debate',
            name='debate_end_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 20, 0, 57, 3, 584189)),
        ),
        migrations.AlterField(
            model_name='debate',
            name='debate_start_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 19, 21, 57, 3, 584189)),
        ),
    ]
