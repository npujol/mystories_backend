from django.db import models
from django.utils.translation import gettext as _

from ..core.models import TimestampedModel

NOTIFICATION_STATUS = (
    ("opened", _("Opened by someone")),
    ("send", _("It was send")),
    ("received", _("Received by someone")),
    ("viewed", _("Viewed by someone")),
    ("closed", _("Closed - not available anymore")),
)


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

    status = models.CharField(
        max_length=32, choices=NOTIFICATION_STATUS, default=NOTIFICATION_STATUS[0]
    )

    def __str__(self):
        return "{}: {}".format(self.author, self.title)
