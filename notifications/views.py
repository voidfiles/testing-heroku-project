import json
import logging

from django.conf import settings
from django.http import HttpResponse

from notifications.google_gcm import send_gcm_message_for_user

logger = logging.getLogger(__name__)

class ApiError(Exception):
    pass


def api_call(requires_auth=True):
    def real_decorator(function):
        def wrapper(request, *args, **kwargs):
            if requires_auth and request.adn_user is None:
                status = 'error'
                code = 403
                data = {'error_message': 'This call requires authentication.'}
            else:
                try:
                    data = function(request, *args, **kwargs)
                    status = 'ok'
                    code = 200
                except ApiError, e:
                    status = 'error'
                    data = {'error_message': unicode(e)}
                    code = 400
                except Exception, e:
                    logger.exception(e)
                    status = 'error'
                    data = {'error_message': 'Unexpected Error'}  
                    code = 500

            resp = json.dumps({
                'meta': {
                    'status': status,
                },
                'data': data,
            })

            return HttpResponse(resp, content_type='application/json', status=code)

        return wrapper
    return real_decorator


@api_call()
def set_channel_id_for_user(request):
    channel_id = request.POST.get('channel_id')
    if not channel_id:
        raise ApiError('Method requires channel_id')

    request.adn_user.gcm_channel_id = channel_id
    request.adn_user.save()

    return {
        'adn_user_id': request.adn_user.adn_user_id,
        'channel_id': channel_id
    }


@api_call()
def update_notification_prefs(request):
    prefs = request.POST.get('prefs')
    if not prefs:
        raise ApiError('Method requires prefs params')

    prefs = prefs.split(',')
    if not prefs:
        raise ApiError('Prefs paramaters seems to be malformed')

    prefs = {pref: True for pref in prefs if pref in settings.VALID_MESSAGE_PREFERENCES}
    request.adn_user.extra['notifications'] = prefs
    request.adn_user.save()

    return {
        'adn_user_id': request.adn_user.adn_user_id,
        'prefs': prefs,
    }


@api_call()
def send_message_for_user(request):
    message = request.POST.get('message')
    if not message:
        raise ApiError('Method requires a message')

    if len(message) > 256:
        raise ApiError('Message can only be 256 characters long')
    print 'yo dawg trying to send a message: %s' % (message)
    send_gcm_message_for_user(request.adn_user, message)

    return {
        'adn_user_id': request.adn_user.adn_user_id,
        'messsage': message
    }