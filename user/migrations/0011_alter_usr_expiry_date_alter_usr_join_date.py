# Generated by Django 4.2.2 on 2023-07-05 12:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_alter_usr_join_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usr',
            name='expiry_date',
            field=models.DateField(default=datetime.date(2023, 8, 4)),
        ),
        migrations.AlterField(
            model_name='usr',
            name='join_date',
            field=models.DateField(default=datetime.date(2023, 7, 5)),
        ),
    ]