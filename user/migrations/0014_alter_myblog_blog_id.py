# Generated by Django 4.2.2 on 2023-07-07 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_remove_myblog_id_myblog_blog_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myblog',
            name='blog_id',
            field=models.CharField(max_length=300, primary_key=True, serialize=False),
        ),
    ]