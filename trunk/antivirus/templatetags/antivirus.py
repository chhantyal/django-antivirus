import random, types

from django import template
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from apps.antivirus.models import File, FILE_STANDING, FILE_VIRUS_NOT_FOUND,\
        FILE_VIRUS_FOUND, FILE_NOT_EXISTS
from apps.antivirus import app_settings

register = template.Library()

@register.filter_function
def check_for_virus(object, field_name):
    file_field = getattr(object, field_name)
    file_path = file_field.path
    url = file_field.url

    file = File.objects.get_or_create_for_object(object, file_path, url)

    if file.status == FILE_VIRUS_FOUND:
        return app_settings.ANTIVIRUS_MSG_VIRUS_FOUND
    elif file.status == FILE_NOT_EXISTS:
        return app_settings.ANTIVIRUS_MSG_FILE_NOT_EXISTS
    elif file.status == FILE_STANDING:
        text = app_settings.ANTIVIRUS_MSG_WAITING
        key = random.randint(1,200000)

        return mark_safe('''<span id="text_for_download_%(key)s">%(text)s</span>
            <script type="text/javascript" defer="defer">
            $('#text_for_download_%(key)s').load('/antivirus/files/%(fid)d/check/');
            </script>
            '''%{
                'key': key,
                'text': text,
                'fid': file.id,
                })
    elif file.status >= FILE_VIRUS_NOT_FOUND:
        file_field = getattr(object, field_name)
        return mark_safe('<a href="%s">%s</a>'%(file_field.url, app_settings.ANTIVIRUS_MSG_DOWNLOAD))

