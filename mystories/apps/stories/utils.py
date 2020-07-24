from os import makedirs, path, remove
from sys import version_info
from uuid import uuid4 as uuid

from celery import shared_task
from django.conf import settings
from django.core.files.base import ContentFile
from gtts import gTTS

FOLDER_DIR = path.join(path.dirname(path.abspath(__file__)), "..")
DIR_NAME = "gTTS"
TEMP_PATH = path.join(
    FOLDER_DIR, path.join(getattr(settings, "MEDIA_URL", " ")[1:], DIR_NAME)
)


class TTSStory:
    def __init__(self, speech):
        self.speech = speech
        self.language = speech.language
        self.story = speech.story
        self.text = self.story_text()

    def story_text(self):
        return (" ").join(
            [
                "Title",
                self.story.title,
                "Author",
                self.story.author.user.username,
                self.story.body,
            ]
        )

    def create(self):

        tts = gTTS(text=self.text, lang=self.language)

        self.speech.speech_file.save(
            self.story.slug + str(uuid()) + ".mp3", ContentFile("")
        )

        self.speech.speech_file.open("wb")
        tts.write_to_fp(self.speech.speech_file)

        self.speech.is_ready = True
        self.speech.save()

        return "Ready"
