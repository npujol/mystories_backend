# Generated by Django 3.1 on 2020-10-08 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("notifications", "0003_auto_20200623_1335")]

    operations = [
        migrations.RemoveField(model_name="notification", name="status"),
        migrations.AddField(
            model_name="notification",
            name="opened",
            field=models.BooleanField(default=False),
        ),
    ]