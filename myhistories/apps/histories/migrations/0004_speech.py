# Generated by Django 3.0.7 on 2020-06-15 09:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("histories", "0003_auto_20200611_1316")]

    operations = [
        migrations.CreateModel(
            name="Speech",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("language", models.CharField(max_length=255)),
                ("url_file", models.URLField(blank=True, null=True)),
                ("state", models.BooleanField(default=False)),
                (
                    "history",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="histories.History",
                    ),
                ),
            ],
            options={"ordering": ["-created_at", "-updated_at"], "abstract": False},
        )
    ]
