from django.conf import settings
from django.db import models
from django.utils.translation import gettext as _

from ..core.models import TimestampedModel

ENGLISH = "en"
SPANISH = "es"
GERMAN = "de"


class Story(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)
    language = models.CharField(
        max_length=2,
        choices=[
            (ENGLISH, _("English")),
            (SPANISH, _("Spanish")),
            (GERMAN, _("German")),
        ],
        default=ENGLISH,
    )
    description = models.TextField(null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    body_markdown = models.TextField(null=True, blank=True)
    image = models.ImageField(
        _("Avatar"),
        upload_to="image/%Y/%m/%d/",
        default="story_default.png",
        null=True,
        blank=True,
    )
    owner = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name=_("stories")
    )
    tags = models.ManyToManyField("stories.Tag", related_name=_("stories"))

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    body = models.TextField()
    story = models.ForeignKey(
        "stories.Story", related_name=_("comments"), on_delete=models.CASCADE
    )
    owner = models.ForeignKey(
        "profiles.Profile", related_name=_("comments"), on_delete=models.CASCADE
    )


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.tag


class Speech(TimestampedModel):
    story = models.OneToOneField("stories.Story", on_delete=models.CASCADE)
    language = models.CharField(max_length=10, null=True, default="en")
    speech_file = models.FileField(upload_to="gTTS/%Y/%m/%d/", null=True, blank=True)
    is_ready = models.BooleanField(default=False, null=True)


def __str__(self):
    return self.story.slug
