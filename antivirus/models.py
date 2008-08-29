import os

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey
from django.utils.translation import ugettext_lazy as _

import app_settings

FILE_STANDING = 0
FILE_VIRUS_NOT_FOUND = 1
FILE_VIRUS_FOUND = -1
FILE_NOT_EXISTS = -2

FILE_STATUS_CHOICES = (
    (FILE_STANDING,        _('Standing')),
    (FILE_VIRUS_NOT_FOUND, _('Virus not found')),
    (FILE_VIRUS_FOUND,     _('Virus found')),
    (FILE_NOT_EXISTS,      _('Not exists')),
)

class FileManager(models.Manager):
    def get_or_create_for_object(self, obj, file_path, url=None):
        ctype = ContentType.objects.get_for_model(obj)
        file, new = self.get_or_create(
                path = file_path,
                defaults = {
                    'content_type': ctype,
                    'object_id': obj.id,
                    'url': url,
                    }
                )

        return file

class File(models.Model):
    path = models.CharField(max_length=250, unique=True)
    status = models.SmallIntegerField(default=0, blank=True, choices=FILE_STATUS_CHOICES)
    content_type = models.ForeignKey(ContentType, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object = GenericForeignKey()
    viruses_found = models.TextField(blank=True)
    url = models.URLField(blank=True, null=True)

    objects = FileManager()

    def __unicode__(self):
        return self.path

    class Meta:
        pass

    def scanfile(self):
        if not self.check_file_exists():
            return False

        if app_settings.ANTIVIRUS_USE_CLAMAV_DEAMON:
            import pyclamd
            if app_settings.ANTIVIRUS_CLAMD_USE_UNIX:
                pyclamd.init_unix_socket(
                        app_settings.ANTIVIRUS_CLAMD_UNIX_PATH,
                        )
            else:
                pyclamd.init_network_socket(
                        app_settings.ANTIVIRUS_CLAMD_HOSTNAME,
                        app_settings.ANTIVIRUS_CLAMD_PORT,
                        )
            found = pyclamd.scan_file(self.path)
            virus = found and '\n'.join(found.values()) or ''
        else:
            import pyclamav
            found, virus = pyclamav.scanfile(self.path)

        if found:
            self.viruses_found = virus
            self.status = FILE_VIRUS_FOUND
            self.save()
        else:
            self.viruses_found = ''
            self.status = FILE_VIRUS_NOT_FOUND
            self.save()

        return found

    def check_file_exists(self):
        if self.status != FILE_NOT_EXISTS and not os.path.isfile(self.path):
            self.status = FILE_NOT_EXISTS
            self.save()
            return False

        elif self.status == FILE_NOT_EXISTS and os.path.isfile(self.path):
            self.status = FILE_STANDING
            self.save()

        return True

