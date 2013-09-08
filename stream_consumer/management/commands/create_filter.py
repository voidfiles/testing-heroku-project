import json
import logging

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from stream_consumer.adn import adn_api

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'Gets, or creates a filter specified in settings'

    def handle(self, *args, **options):
        adn_api.add_authorization_token(settings.ADN_USER_ACCESS_TOKEN)

        resp = adn_api.get('/filters')
        if resp.status_code != 200:
            raise CommandError('Getting filters for user failed: %s' % resp.content)

        existing_filter = None
        for _filter in resp.json()['data']:
            if _filter['name'] == settings.ADN_FILTER_SCHEMA['name']:
                existing_filter = _filter

        if existing_filter:
            resp = adn_api.put_json('/filters/%s' % (existing_filter['id']), data=settings.ADN_FILTER_SCHEMA)
        else:
            resp = adn_api.post_json('/filters', data=settings.ADN_FILTER_SCHEMA)

        # print resp.json()

        if resp.status_code != 200:
            raise CommandError('Updating or creating filter failed: %s' % resp.content)

        print 'Your Filter ID: %s' % resp.json()['data']['id']


