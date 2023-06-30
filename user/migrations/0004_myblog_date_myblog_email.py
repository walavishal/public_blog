# Generated by Django 4.2.2 on 2023-06-28 06:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_rename_users_usr'),
    ]

    operations = [
        migrations.AddField(
            model_name='myblog',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='myblog',
            name='email',
            field=models.CharField(default='', max_length=600),
        ),
    ]
