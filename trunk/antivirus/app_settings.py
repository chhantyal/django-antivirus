from django.conf import settings
from django.utils.translation import ugettext as _

ANTIVIRUS_BACKEND = getattr(settings, 'ANTIVIRUS_BACKEND', 'antivirus.backends.ClamAV')

ANTIVIRUS_MSG_VIRUS_FOUND = _("You can't download this file because we found a virus in it.")
ANTIVIRUS_MSG_FILE_NOT_EXISTS = _("You can't download this file because it not either exists.")
ANTIVIRUS_MSG_WAITING = _('Wait while checking for virus...')
ANTIVIRUS_MSG_SOMETHING_WRONG = _("You can't download this file because we found something wrong in it.")
ANTIVIRUS_MSG_DOWNLOAD = _('Click to download')

ANTIVIRUS_USE_CLAMAV_DEAMON = getattr(settings, 'ANTIVIRUS_USE_CLAMAV_DEAMON', False)
ANTIVIRUS_CLAMD_USE_UNIX = getattr(settings, 'ANTIVIRUS_CLAMD_USE_UNIX', False)
ANTIVIRUS_CLAMD_HOSTNAME = getattr(settings, 'ANTIVIRUS_CLAMD_HOSTNAME', 'localhost')
ANTIVIRUS_CLAMD_PORT = getattr(settings, 'ANTIVIRUS_CLAMD_PORT', 3310)
ANTIVIRUS_CLAMD_UNIX_PATH = getattr(settings, 'ANTIVIRUS_CLAMD_UNIX_PATH', '/var/run/clamav/clamd.ctl')

