#! /bin/bash
python manage.py run_gunicorn -b 0.0.0.0:$PORT & python manage.py start_stream 