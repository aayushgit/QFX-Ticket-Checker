from django.apps import AppConfig
from .models import *


class QfxticketsConfig(AppConfig):
    name = 'QFXTickets'

    def ready(self):
        NowShowing = self.get_model('NowShowing')
        Emails = self.get_model('Emails')
