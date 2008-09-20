from django.http import HttpResponse
from django.utils.translation import ugettext as _

from models import File, FILE_STANDING, FILE_VIRUS_NOT_FOUND,\
        FILE_VIRUS_FOUND, FILE_NOT_EXISTS
import app_settings

def file_check(request, file_id):
    """Checks a file and returns HTML respective to if it found virus or not"""
    text = request.GET.get('text', _('Click to Download'))

    try:
        f = File.objects.get(id=file_id)
    except File.DoesNotExist, e:
        return HttpResponse(app_settings.ANTIVIRUS_MSG_FILE_NOT_EXISTS)

    f.scanfile()

    if f.status == FILE_VIRUS_NOT_FOUND:
        return HttpResponse('<a href="%s">%s</a>'%(f.url, text))
    elif f.status == FILE_VIRUS_FOUND:
        return HttpResponse(app_settings.ANTIVIRUS_MSG_VIRUS_FOUND)

    return HttpResponse(app_settings.ANTIVIRUS_MSG_SOMETHING_WRONG)

