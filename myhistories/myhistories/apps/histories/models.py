from django.db import models

from myhistories.apps.core.models import TimestampedModel


class History(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)

    description = models.TextField()
    body = models.TextField()

    # Every history must have an author. This will answer questions like "Who
    # gets credit for writing this history?" and "Who can edit this history?".
    # Unlike the `User` <-> `Profile` relationship, this is a simple foreign
    # key (or one-to-many) relationship. In this case, one `Profile` can have
    # many `History`s.
    author = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name="histories"
    )

    tags = models.ManyToManyField("histories.Tag", related_name="histories")

    def __str__(self):
        return self.title


class Comment(TimestampedModel):
    body = models.TextField()

    history = models.ForeignKey(
        "histories.History", related_name="comments", on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        "profiles.Profile", related_name="comments", on_delete=models.CASCADE
    )


class Tag(TimestampedModel):
    tag = models.CharField(max_length=255)
    slug = models.SlugField(db_index=True, unique=True)

    def __str__(self):
        return self.tag
