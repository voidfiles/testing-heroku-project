

## Getting Started

```sh
>>> virtualenv venv --distribute --no-site-packages
>>> source venv/bin/activate
>>> pip install -r requirements.txt

>>> heroku create
>>> heroku addons:add memcachier:dev # Memcache addon for storing Google Access tokens
```

Now you will need to create a .env file with some configuration variables.

```
ADN_CLIENT_ID=<From https://account.app.net/developer/apps/>
ADN_CLIENT_SECRET=<From https://account.app.net/developer/apps/>
```

For the app token, we will run a command

```
>>> foreman run python manage.py get_app_token
Your App.net App Token: <Your App Token>
# Add to your .env file: ADN_APP_TOKEN=<Your App Token>
```

From your App.net App's detail page you can generate a user access token for your self.

```
ADN_USER_ACCESS_TOKEN=<From https://account.app.net/developer/apps/>
```

Once you have added all the other data we can create a stream filter that will determine what app stream messages you will recieve.
By default the filter, and stream are configured like this:

```py
ADN_FILTER_SCHEMA = {
    'clauses': [
        {
            'field': u'/data/entities/mentions/*/id',
            'object_type': u'post',
            'operator': 'one_of',
            'value': u'$authorized_userids'
        }, {
            'field': u'/data/follows_user/id',
            'object_type': u'user_follow',
            'operator': 'one_of',
            'value': u'$authorized_userids'
        }, {
            'field': u'/data/post/user/id',
            'object_type': u'star',
            'operator': 'one_of',
            'value': u'$authorized_userids'
        }, {
            'field': u'/data/repost_of/user/id',
            'object_type': u'post',
            'operator': 'one_of',
            'value': u'$authorized_userids'
        }, {
            'field': u'/data/user/id',
            'object_type': u'mute',
            'operator': 'one_of',
            'value': u'$authorized_userids'
        }, {
            'field': u'/meta/channel_type',
            'object_type': u'message',
            'operator': 'equals',
            'value': u'net.app.core.pm'
        }, {
            'field': u'/meta/channel_type',
            'object_type': u'message',
            'operator': 'equals',
            'value': u'net.app.core.broadcast'
        }
    ],
    'match_policy': 'include_any',
    'name': u'my_users_actions',
}

ADN_STREAM_SCHEMA = {
    "object_types": [
        "star",
        "user_follow",
        "message",
        "channel",
    ],
    "type": "long_poll",
    "key": os.environ.get('ADN_STREAM_NAME', 'my_users_actions_dev')
}
```

You can find documentation on [filters](http://developers.app.net/docs/resources/filter/), and [stream schemas](http://developers.app.net/docs/resources/app-stream/) on the developer docs.

Once you have modified the schemas to fit your needs you can create the filter by running the following command.

```
foreman run python manage.py create_filter
Your Filter ID: <Your Filter ID>
# Add to your .env file: ADN_STREAM_FILTER_ID=<Your Filter ID>
```

If you wish to use this to do [Google Cloud Messaging for Chrome](http://developer.chrome.com/apps/cloudMessaging.html). You will need to follow the instructions to set that up. And add the following variables to your .env file.

```
GCM_CLIENT_ID=
GCM_CLIENT_SECRET=
GCM_REFRESH_TOKEN=
```

Once you have finished creating your .env file you will want to make sure those variables get pushed to heroku. To make your life easier we are using a config plugin.

```sh
>>> heroku plugins:install git://github.com/ddollar/heroku-config.git
heroku-config installed
```

Now you can push whats in your .env file to your heroku enviroment

**Note this will overwrite variables if they are already defined in your Heroku enviroment**

```sh
>>> heroku config:push
```

## Running In Dev Mode

```
foreman start
```

Here you can see that a web interface and a streaming consumer will start. If everything is setup you should begin to receive messages from the App.net stream.


## Deploying

git push heroku master




