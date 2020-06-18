from celery import shared_task

from .models import Speech, History
from .utils import TTSHistory


@shared_task(name="Create a speech from an history")
def create_speech(history__slug):

    history = History.objects.get(slug=history__slug)
    speech, _ = Speech.objects.get_or_create(history=history, language="en")

    tts = TTSHistory(speech)
    tts.create()

    return "The speech for the history: {} is ready".format(history.slug)
