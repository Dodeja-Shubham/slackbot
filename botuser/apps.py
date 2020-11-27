from django.apps import AppConfig


class BotuserConfig(AppConfig):
    name = 'botuser'

    def ready(self):
        import botuser.signals