from django.db import models
from django.utils.translation import gettext as _

from ..core.models import TimestampedModel


class Notification(TimestampedModel):
    title = models.CharField(db_index=True, max_length=255)
    body = models.TextField()

    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name=_("notification")
    )

    receivers = models.ManyToManyField(
        "profiles.Profile", related_name=_("notifications")
    )

    def __str__(self):
        return self.title
