import random, types

from django import template
from django.utils.translation import ugettext as _
from django.utils.safestring import mark_safe

from antivirus.models import File, FILE_STANDING, FILE_VIRUS_NOT_FOUND,\
        FILE_VIRUS_FOUND, FILE_NOT_EXISTS
from antivirus import app_settings

register = template.Library()

def generic_check_virus(obj, field_name, url=None):
    file_field = getattr(obj, field_name)
    file_path = file_field.path
    url = url or file_field.url

    file = File.objects.get_or_create_for_object(obj, file_path, url)

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
        file_field = getattr(obj, field_name)
        return mark_safe('<a href="%s">%s</a>'%(
            url,
            app_settings.ANTIVIRUS_MSG_DOWNLOAD,
            ))

@register.filter_function
def check_for_virus(obj, field_name):
    """Uses this template filter to print the HTML for download the file just
    after check for virus. If a virus be found, it won't show the link to download.
    
    Example:
        
    {{ object|check_for_virus:"file_field_name" }}
    """
    return generic_check_virus(obj, field_name)

class CheckVirusRender(template.Node):
    vobj = None
    vattr = None
    vurl = None

    def __init__(self, obj, attr, url=None):
        self.vobj = template.Variable(obj)
        self.vattr = template.Variable(attr)
        self.vurl = template.Variable(url)

    def render(self, context):
        obj = self.vobj.resolve(context)
        attr = self.vattr.resolve(context)
        url = self.vurl.resolve(context)

        ret = generic_check_virus(obj, attr, url)

        return ret

def do_check_virus(parser, token):
    try:
        parts = token.split_contents()

        obj = parts[1]
        attr = parts[2]
        
        url = len(parts) > 3 and parts[3] or None
    except IndexError, e:
        raise template.TemplateSyntaxError, "%s requires 2 or 3 arguments (object, attribute name and url - optionally)" \
                % token.contents.split()[0]

    return CheckVirusRender(obj, attr, url)

register.tag('check_virus', do_check_virus)

