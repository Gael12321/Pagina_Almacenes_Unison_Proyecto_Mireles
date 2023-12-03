"""
ASGI config for Pagina_Almacenes_Unison project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Pagina_Almacenes_Unison.settings')

application = get_asgi_application()
