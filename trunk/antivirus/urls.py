from django.conf.urls.defaults import *

from views import file_check

urlpatterns = patterns('',
    (r'^files/(?P<file_id>\d+)/check/$', file_check, {}, 'antivirus_file_check'),
)
