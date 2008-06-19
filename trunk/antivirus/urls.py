from django.conf.urls.defaults import *

urlpatterns = patterns('apps.antivirus.views',
    (r'^files/(?P<file_id>\d+)/check/$', 'file_check'),
)
