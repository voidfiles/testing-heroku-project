from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^user/channel', 'notifications.views.set_channel_id_for_user', name='set_channel_id_for_user'),
    url(r'^user/message', 'notifications.views.send_message_for_user', name='send_message_for_user'),
    url(r'^user/preferences', 'notifications.views.update_notification_prefs', name='update_notification_prefs'),
)
