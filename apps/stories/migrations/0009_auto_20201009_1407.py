# Generated by Django 3.1 on 2020-10-09 14:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("stories", "0008_auto_20200729_1612")]

    operations = [
        migrations.RenameField(
            model_name="comment", old_name="author", new_name="owner"
        ),
        migrations.RenameField(model_name="story", old_name="author", new_name="owner"),
    ]
