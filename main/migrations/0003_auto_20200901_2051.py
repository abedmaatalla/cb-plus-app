# Generated by Django 2.2.1 on 2020-09-01 20:51

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20200901_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='syncrecord',
            name='action_at',
            field=models.DateField(default=datetime.datetime(2020, 9, 1, 20, 51, 53, 390325, tzinfo=utc)),
        ),
    ]