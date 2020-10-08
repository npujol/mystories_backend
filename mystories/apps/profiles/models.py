from django.db import models
from django.utils.translation import gettext as _

from ..core.models import TimestampedModel


class Profile(TimestampedModel):
    user = models.OneToOneField("authentication.User", on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(
        _("Avatar"), upload_to="image/%Y/%m/%d/", null=True, blank=True
    )
    follows = models.ManyToManyField(
        "self", related_name="followed_by", symmetrical=False
    )

    favorites = models.ManyToManyField("stories.Story", related_name="favorited_by")

    def __str__(self):
        return self.user.username

    def follow(self, profile):
        """Follow `profile` if we're not already following `profile`."""
        self.follows.add(profile)

    def unfollow(self, profile):
        """Unfollow `profile` if we're already following `profile`."""
        self.follows.remove(profile)

    def is_following(self, profile):
        """Returns True if we're following `profile`; False otherwise."""
        return self.follows.filter(pk=profile.pk).exists()

    def is_followed_by(self, profile):
        """Returns True if `profile` is following us; False otherwise."""
        return self.followed_by.filter(pk=profile.pk).exists()

    def favorite(self, story):
        """Favorite `story` if we haven't already favorited it."""
        self.favorites.add(story)

    def unfavorite(self, story):
        """Unfavorite `story` if we've already favorited it."""
        self.favorites.remove(story)

    def has_favorited(self, story):
        """Returns True if we have favorited `story`; else False."""
        return self.favorites.filter(pk=story.pk).exists()
