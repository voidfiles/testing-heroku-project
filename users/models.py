from datetime import timedelta, datetime
import pytz

from django.db import models
from jsonfield import JSONField


class UserManager(models.Manager):
    def update_user(self, user, raw_user_object):
        user.extra['raw_user_object'] = raw_user_object
        user.save()


class User(models.Model):
    adn_user_id = models.IntegerField()
    access_token = models.CharField(max_length=256, null=True, blank=True)
    gcm_channel_id = models.CharField(max_length=256, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    extra = JSONField()

    objects = UserManager()

    @property
    def needs_update(self):
        if pytz.UTC.localize(datetime.now() - timedelta(minutes=60)) > self.updated:
            return True
        return False

    @property
    def notifications(self):
        return self.extra.get('notifications', {});
