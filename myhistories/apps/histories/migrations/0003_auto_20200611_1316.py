# Generated by Django 3.0.7 on 2020-06-11 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('histories', '0002_auto_20200604_1330'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='slug',
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
