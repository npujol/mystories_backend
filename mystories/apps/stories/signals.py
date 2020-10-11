import markdown
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext as _
from rest_framework.exceptions import NotFound

from ..core.utils import generate_random_string
from ..notifications.models import Notification
from .models import Speech, Story


@receiver(pre_save, sender=Story)
def add_slug_to_story_if_not_exists(sender, instance, *args, **kwargs):
    MAXIMUM_SLUG_LENGTH = 255

    if instance and not instance.slug:
        slug = slugify(instance.title)
        unique = generate_random_string()

        if len(slug) > MAXIMUM_SLUG_LENGTH:
            slug = slug[:MAXIMUM_SLUG_LENGTH]

        while len(slug + "-" + unique) > MAXIMUM_SLUG_LENGTH:
            parts = slug.split("-")

            if len(parts) == 1:
                slug = slug[: MAXIMUM_SLUG_LENGTH - len(unique) - 1]
            else:
                slug = "-".join(parts[:-1])

        instance.slug = slug + "-" + unique


@receiver(pre_save, sender=Story)
def add_body_markdown(sender, instance, *args, **kwargs):
    instance.body = markdown.markdown(instance.body_markdown)
    print(instance.body)


@receiver(pre_save, sender=Speech)
def on_change(sender, instance: Speech, **kwargs):
    if instance.id is None:
        return

    previous = Speech.objects.get(id=instance.id)
    if previous.is_ready != instance.is_ready:
        Notification.objects.create(
            title=_("The speech is ready"),
            body=_("The speech for the story: {} is ready".format(previous.story.slug)),
            sender=previous.story.owner,
            owner=previous.story.owner,
        )
