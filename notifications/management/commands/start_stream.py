import logging

from django.core.management.base import BaseCommand
from django.conf import settings

from stream_consumer.adn import adn_api
from stream_consumer.stream import StreamListener, Stream
from notifications.google_gcm import send_gcm_message_for_user
from users.models import User


logger = logging.getLogger(__name__)


class NotifcationStreamListener(StreamListener):

    def on_user_follow(self, data, meta):
        if meta.get('is_deleted') == True:
            return
        print 'User follow: %s' % meta
        to_user_id = int(data['follows_user']['id'])
        from_user_id = int(data['user']['id'])

        user = User.objects.filter(adn_user_id=to_user_id)
        if not user.count():
            return

        notification = {
            'type': 'follow',
            'from_user_id': from_user_id,
            'to_user_id': to_user_id,
        }

        send_gcm_message_for_user(user[0], notification)


    def on_post_action(self, data, meta, msg_type):
        if meta.get('is_deleted') == True:
            return
        print 'Post action: %s' % meta
        post_id = data['post']['id']
        to_user_id = int(data['post']['user']['id'])
        from_user_id = data['user']['id']

        user = User.objects.filter(adn_user_id=to_user_id)
        if not user.count():
            return

        notification = {
            'type': 'star',
            'post_id': post_id,
            'from_user_id': from_user_id
        }

        send_gcm_message_for_user(user[0], notification)

    def on_repost(self, data, meta):
        return self.on_post_action(data, meta, 'repost')

    def on_star(self, data, meta):
        return self.on_post_action(data, meta, 'star')

    def on_message(self, data, meta):
        if meta.get('is_deleted') == True:
            return

        if meta.get('channel_type') not in ('net.app.core.broadcast', 'net.app.core.pm'):
            return

        if meta.get('channel_type') == 'net.app.core.broadcast':
            notif_type = 'alert'
        else:
            notif_type = 'pm'

        print 'Got a message: %s' % (meta)
        notification = {
            'type': notif_type,
            'channel_id': data.get('channel_id'),
            'id': data.get('id'),
        }

        user_ids = map(int, meta.get('subscribed_user_ids', []))
        print 'Sending a message: %s to users: %s' % (notification, user_ids)
        users = User.objects.filter(adn_user_id__in=user_ids)

        if not users:
            return

        for user in users:
            send_gcm_message_for_user(user, notification)


    def on_fallback(self, data, meta):
        # print 'Got an unhandled message meta: %s' % (meta)
        pass


class Command(BaseCommand):
    args = ''
    help = 'Creates, or updates a stream and then starts consuming the stream'

    def handle(self, *args, **options):
        adn_api.add_authorization_token(settings.ADN_APP_TOKEN)

        listener = NotifcationStreamListener()
        stream = Stream(adn_api, settings.ADN_STREAM_SCHEMA, listener)
        stream.start()