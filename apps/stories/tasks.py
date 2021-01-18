from celery import shared_task

from .models import Speech, Story
from .tts import TTSStory


@shared_task(name="Create a speech from a story")
def create_speech(story__slug):

    story = Story.objects.get(slug=story__slug)
    speech, _ = Speech.objects.get_or_create(story=story, language="en")

    tts = TTSStory(speech)
    tts.create()

    return "The speech for the story: {} is ready".format(story.slug)
