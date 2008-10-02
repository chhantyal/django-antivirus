# django-antivirus setup

from distutils.core import setup
from antivirus import get_version

setup(
    name = 'django-antivirus',
    version = get_version(),
    description = 'Antivirus Django pluggable application',
    long_description = 'django-antivirus is a pluggable application for Django Web Framework that works with ClamAV.',
    author = 'Marinho Brandao',
    author_email = 'marinho@gmail.com',
    url = 'http://django-antivirus.googlecode.com',
    download_url = 'http://code.google.com/p/django-antivirus/downloads/list',
    license = 'GNU Lesser General Public License (LGPL)',
    packages = ['antivirus', 'antivirus.templatetags'],
)
