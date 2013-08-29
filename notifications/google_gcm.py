import json
import requests
from django.core.cache import cache
from django.conf import settings


def get_access_token():
    access_token = cache.get('access_token')
    if not access_token:
        resp = requests.post("https://accounts.google.com/o/oauth2/token", data=dict(
            client_id=settings.GCM_CLIENT_ID,
            client_secret=settings.GCM_CLIENT_SECRET,
            refresh_token=settings.GCM_REFRESH_TOKEN,
            grant_type='refresh_token',
        ))

        if resp.status_code != 200:
            raise Exception("Trouble getting access token https://accounts.google.com/o/oauth2/token %s" % (settings.GCM_CLIENT_ID))

        access_token = resp.json()['access_token']
        cache.set('access_token', access_token, 3600)

    return access_token


def send_gcm_message(channelId, msg=''):
    access_token = get_access_token()
    payload = json.dumps(dict(
        channelId=channelId,
        subchannelId=0,
        payload=msg,
    ))

    resp = requests.post('https://www.googleapis.com/gcm_for_chrome/v1/messages', headers={
        'Content-Type': 'application/json',
        'Authorization': 'Bearer %s' % (access_token)
    }, data=payload)
