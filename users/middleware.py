import hashlib
import json
import logging

import requests

from django.conf import settings
from users.models import User


logger = logging.getLogger(__name__)

class ADNTokenAuthMiddleware(object):
    def fetch_user_data(self, access_token):
        headers = {
            'Authorization': 'Bearer %s' % access_token,
        }

        resp = requests.get('https://alpha-api.app.net/stream/0/token', headers=headers)
        if resp.status_code == 200:
            token = json.loads(resp.content)
            if token.get('data') and token['data'].get('app', {}).get('client_id') == settings.ADN_CLIENT_ID:
                return token['data']
            else:
                logger.error("Failed to find a user object: %s", token)
        else:
            logger.error("Failed to get a user token: %s", resp.content)

        return None

    def process_request(self, request):
        '''Try and setup user for this request'''

        adn_user = None
        token = None
        authorization_header = request.META.get('HTTP_AUTHORIZATION')
        if authorization_header:
            method, access_token = authorization_header.split(' ', 1)
            if access_token:
                logger.info('found an access_token: %s', access_token)
                adn_user = User.objects.filter(access_token=access_token)
                if not adn_user.count():
                    token = self.fetch_user_data(access_token)
                    if token:
                        logger.info('Creating a new user: %s', token)
                        adn_user, created = User.objects.get_or_create(adn_user_id=token['user']['id'], defaults={
                            'access_token': access_token,
                            'extra': {
                                'raw_user_object': token['user']
                            }
                        })
                    else:
                        logger.error("Failed to create user from token: %s", token)
                else:
                    adn_user = adn_user[0]

                if adn_user.needs_update:
                    if token is None:
                        token = self.fetch_user_data(access_token)

                    User.objects.update_user(adn_user, token['user'])

        request.adn_user = adn_user


        return None

