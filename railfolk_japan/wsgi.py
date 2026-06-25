"""WSGI config for railfolk_japan."""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railfolk_japan.settings")

application = get_wsgi_application()
