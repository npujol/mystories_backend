from django.apps import AppConfig


class HistoriesConfig(AppConfig):
    name = "apps.stories"

    def ready(self):
        import apps.stories.signals
