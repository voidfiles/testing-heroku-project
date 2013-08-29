import json
import requests


class ADNSession(requests.Session):
    def request(self, method, url, *args, **kwargs):
        if url:
            url = 'https://alpha-api.app.net/stream/0' + url
        return super(ADNSession, self).request(method, url, *args, **kwargs)

    def add_authorization_token(self, token):
        self.headers.update({
            'Authorization': 'Bearer %s' % (token),
        })

    def request_json(self, method, *args, **kwargs):
        kwargs.setdefault('headers', dict())
        kwargs.setdefault('data', dict())
        kwargs['headers'].update({'Content-Type': 'application/json'})
        kwargs['data'] = json.dumps(kwargs['data'])
        return self.request(method, *args, **kwargs)

    def post_json(self, *args, **kwargs):
        return self.request_json('post', *args, **kwargs)

    def put_json(self, *args, **kwargs):
        return self.request_json('put', *args, **kwargs)

# resp = adn_api.get('/posts')
# resp = adn_api.post('/posts', data={'text': 'awesome'})
# resp = adn_api.post_json('/posts', data={'text': 'awesome'})
adn_api = ADNSession()