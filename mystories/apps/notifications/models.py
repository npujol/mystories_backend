from django.db import models
from django.utils.translation import gettext as _

from ..core.models import TimestampedModel


class Notification(TimestampedModel):
    title = models.CharField(db_index=True, max_length=255)
    body = models.TextField()

    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name=_("notification")
    )

    receiver = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
        related_name=_("mynotification"),
        null=True,
    )

    opened = models.BooleanField(default=False)

    def __str__(self):
        return "{}: {}".format(self.author, self.title)
