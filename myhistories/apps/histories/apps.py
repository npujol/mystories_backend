from django.apps import AppConfig


class HistoriesConfig(AppConfig):
    name = "apps.histories"

    def ready(self):
        import apps.histories.signals
