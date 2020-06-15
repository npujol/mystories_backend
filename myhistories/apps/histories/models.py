from django.db import models
from django.utils.translation import gettext as _


from ..core.models import TimestampedModel


class History(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)

    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name=_("histories")
    )

    tags = models.ManyToManyField("histories.Tag", related_name=_("histories"))

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    body = models.TextField()

    history = models.ForeignKey(
        "histories.History", related_name=_("comments"), on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        "profiles.Profile", related_name=_("comments"), on_delete=models.CASCADE
    )


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tag


class Speech(TimestampedModel):
    history = models.OneToOneField("histories.History", on_delete=models.CASCADE)
    language = models.CharField(max_length=255,)
    url_file = models.URLField(blank=True, null=True)
    state = models.BooleanField(default=False)


def __str__(self):
    return self.history.slug
