# Generated by Django 3.0.7 on 2020-06-15 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("stories", "0004_speech")]

    operations = [
        migrations.RemoveField(model_name="speech", name="url_file"),
        migrations.AddField(
            model_name="speech",
            name="speech_file",
            field=models.FileField(blank=True, null=True, upload_to="gTTS/%Y/%m/%d/"),
        ),
    ]
