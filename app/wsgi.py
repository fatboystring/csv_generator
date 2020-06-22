"""
WSGI config for csv_generator project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")

application = get_wsgi_application()
