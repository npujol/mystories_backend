from celery import shared_task

from .models import Speech, Story
from .utils import TTSHistory


@shared_task(name="Create a speech from an story")
def create_speech(history__slug):

    story = Story.objects.get(slug=history__slug)
    speech, _ = Speech.objects.get_or_create(story=story, language="en")

    tts = TTSHistory(speech)
    tts.create()

    return "The speech for the story: {} is ready".format(story.slug)
