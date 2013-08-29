import logging

import requests

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = 'Gets an App.net App Token from the API'

    def handle(self, *args, **options):
        resp = requests.post('https://account.app.net/oauth/access_token', data=dict(
            client_id=settings.ADN_CLIENT_ID,
            client_secret=settings.ADN_CLIENT_SECRET,
            grant_type='client_credentials'
        ))

        if resp.status_code != 200:
            raise CommandError('Getting App.net App Token failed resp: %s' % resp.content)

        print 'Your App.net App Token: %s' % resp.json()['access_token']