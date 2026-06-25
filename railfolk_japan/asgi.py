"""ASGI config for railfolk_japan."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "railfolk_japan.settings")

application = get_asgi_application()
