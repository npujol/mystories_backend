from django.db import models
from django.utils.translation import gettext as _

from ..core.models import TimestampedModel


class Notification(TimestampedModel):
    title = models.CharField(db_index=True, max_length=255)
    body = models.TextField()

    sender = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
        related_name=_("notification"),
        null=True,
    )

    owner = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
        related_name=_("mynotification"),
        null=True,
    )

    opened = models.BooleanField(default=False)
    optional = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return "{}: {}".format(self.owner, self.title)
