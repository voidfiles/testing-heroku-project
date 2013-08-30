import json
import logging
import requests
import time

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from stream_consumer.adn import adn_api
from stream_consumer.stream import StreamListener, Stream
from notifications.google_gcm import send_gcm_message_for_user
from users.models import User


logger = logging.getLogger(__name__)


class NotifcationStreamListener(StreamListener):

    def on_message(self, data, meta):
        if meta.get('is_deleted') == True:
            return

        if meta.get('channel_type') != 'net.app.core.broadcast':
            return
        print 'Got a message: %s' % (meta)
        notification = json.dumps({
            'channel_id': data.get('channel_id'),
            'id': data.get('id'),
        })

        user_ids = map(int, meta.get('subscribed_user_ids', [3]))
        print 'Sending a message: %s to users: %s' % (notification, user_ids)
        users = User.objects.filter(adn_user_id__in=user_ids)

        if not users:
            return

        for user in users:
            send_gcm_message_for_user(user, notification)


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