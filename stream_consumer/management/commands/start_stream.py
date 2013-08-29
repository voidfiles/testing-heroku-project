import json
import logging
import requests
import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from stream_consumer.adn import adn_api
from stream_consumer.stream import StreamListener, Stream

logger = logging.getLogger(__name__)


class NotifcationStreamListener(StreamListener):

    def on_fallback(self, data, meta):
        pass


class Command(BaseCommand):
    args = ''
    help = 'Creates, or updates a stream and then starts consuming the stream'

    def handle(self, *args, **options):
        adn_api.add_authorization_token(settings.ADN_APP_TOKEN)

        listener = NotifcationStreamListener()
        stream = Stream(adn_api, settings.ADN_STREAM_SCHEMA, listener)
        stream.start()