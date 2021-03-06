# Generated by Django 3.0.7 on 2020-06-23 12:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("profiles", "0002_auto_20200608_1825")]

    operations = [
        migrations.CreateModel(
            name="Notification",
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
                ("title", models.CharField(db_index=True, max_length=255)),
                ("body", models.TextField()),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="notification",
                        to="profiles.Profile",
                    ),
                ),
                (
                    "receivers",
                    models.ManyToManyField(
                        related_name="notifications", to="profiles.Profile"
                    ),
                ),
            ],
            options={"ordering": ["-created_at", "-updated_at"], "abstract": False},
        )
    ]
