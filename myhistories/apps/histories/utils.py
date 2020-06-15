from os import path, makedirs, remove
from sys import version_info
from uuid import uuid4 as uuid

from gtts import gTTS

from celery import shared_task

from django.conf import settings


FOLDER_DIR = path.join(path.dirname(path.abspath(__file__)), "..")
DIR_NAME = "gTTS"
TEMP_PATH = path.join(
    FOLDER_DIR, path.join(getattr(settings, "STATIC_URL", " ")[1:], DIR_NAME)
)


class TTSHistory:
    def __init__(self, speech):
        self.speech = speech
        self.language = speech.language
        self.history = speech.history
        self.filename = speech

        self.text = self.history_text()

    # @shared_task
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

    # @shared_task
    def create(self):
        for h, a in {"language": self.language, "text": self.text}.items():
            if not isinstance(a, str):  # check if receiving a string
                raise (TypeError("TTSHistory.create(%s) takes string" % h))

        if not path.isdir(TEMP_PATH):  # creating temporary directory
            makedirs(TEMP_PATH) if version_info.major == 2 else makedirs(
                # makedirs in py2 missing exist_ok
                TEMP_PATH,
                exist_ok=True,
            )

        tts = (
            gTTS(self.text)
            if self.language == "skip"
            else gTTS(self.text, lang=self.language)
        )
        while True:  # making sure audio file name is truly unique
            fname = str(uuid()) + ".mp3"
            abp_fname = path.join(TEMP_PATH, fname)
            if not path.isfile(abp_fname):
                break
        tts.save(abp_fname)

        self.speech.url_file = "/".join([DIR_NAME, fname])
        self.speech.state = True
        self.speech.save()

        return "/".join([DIR_NAME, fname])
