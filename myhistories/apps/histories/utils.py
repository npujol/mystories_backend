from os import path, makedirs, remove
from sys import version_info
from uuid import uuid4 as uuid

from gtts import gTTS

from celery import shared_task
from django.core.files.base import ContentFile

from django.conf import settings


FOLDER_DIR = path.join(path.dirname(path.abspath(__file__)), "..")
DIR_NAME = "gTTS"
TEMP_PATH = path.join(
    FOLDER_DIR, path.join(getattr(settings, "MEDIA_URL", " ")[1:], DIR_NAME)
)


class TTSHistory:
    def __init__(self, speech):
        self.speech = speech
        self.language = speech.language
        self.history = speech.history
        self.text = self.history_text()

    def history_text(self):
        return (" ").join(
            [
                "Title",
                self.history.title,
                "Author",
                self.history.author.user.username,
                self.history.body,
            ]
        )

    def create(self):

        tts = gTTS(text=self.text, lang=self.language)

        self.speech.speech_file.save(
            self.history.slug + str(uuid()) + ".mp3", ContentFile("")
        )

        self.speech.speech_file.open("wb")
        tts.write_to_fp(self.speech.speech_file)

        self.speech.is_ready = True
        self.speech.save()

        return "Ready"
