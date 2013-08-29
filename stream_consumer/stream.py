import json
import requests
from threading import Thread


class StreamListener(object):

    def on_connect(self):
        """Called once connected to streaming server.

        This will be invoked once a successful response
        is received from the server. Allows the listener
        to perform some work prior to entering the read loop.
        """
        pass

    def on_data(self, raw_data):
        """Called when raw data is received from connection.

        Override this method if you wish to manually handle
        the stream data. Return False to stop stream and close connection.
        """
        data = json.loads(raw_data)

        message_type = data['meta'].get('type')
        method_name = 'on_%s' % (message_type,)
        func = getattr(self, method_name, self.on_fallback)

        func(data['data'], data['meta'])

    def on_fallback(self, data, meta):
        """Called when there is no specific method for handling an object type"""
        return

    def on_limit(self, track):
        """Called when a limitation notice arrvies"""
        return

    def on_error(self, status_code):
        """Called when a non-200 status code is returned"""
        return False

    def on_timeout(self):
        """Called when stream connection times out"""
        return

    def on_disconnect(self, notice):
        """Called when App.net sends a disconnect notice
        """
        return


class Stream(object):

    def __init__(self, api, stream_defenition, listener, **options):
        self.api = api
        self.listener = listener
        self.stream_defenition = stream_defenition
        self.running = False
        self.timeout = options.get("timeout", 600.0)
        self.retry_count = options.get("retry_count", 10)
        self.retry_time = options.get("retry_time", 10.0)
        self.snooze_time = options.get("snooze_time",  5.0)

    def _run(self):
        resp = self.api.get('/streams', params={'key': self.stream_defenition['key']})
        if resp.status_code != 200:
            raise Exception('Getting streams for token failed: %s' % resp.content)

        if resp.json()['data']:
            streaming_endpoint = resp.json()['data'][0]['endpoint']
        else:
            resp = self.api.post_json('/streams', data=self.stream_defenition)
            if resp.status_code != 200:
                raise Exception('Creating a stream failed: %s' % resp.content)

            streaming_endpoint = resp.json()['data']['endpoint']

        # Connect and process the stream
        error_counter = 0
        conn = None
        exception = None
        while self.running:
            if self.retry_count is not None and error_counter > self.retry_count:
                # quit if error count greater than retry count
                break
            try:
                resp = requests.get(streaming_endpoint, stream=True, timeout=self.timeout)
                if resp.status_code != 200:
                    if self.listener.on_error(resp.status_code) is False:
                        break
                    error_counter += 1
                    sleep(self.retry_time)
                else:
                    error_counter = 0
                    self.listener.on_connect()
                    self._read_loop(resp)
            except Exception, exception:
                # any other exception is fatal, so kill loop
                break

        # cleanup
        self.running = False

        if exception:
            raise

    def _data(self, data):
        if self.listener.on_data(data) is False:
            self.running = False

    def _read_loop(self, resp):

        while self.running:

            for line in resp.iter_lines(chunk_size=1):
                if line:
                    self._data(line)


    def start(self, async=False):
        self.running = True
        if async:
            Thread(target=self._run).start()
        else:
            self._run()

    def disconnect(self):
        if self.running is False:
            return
        self.running = False
