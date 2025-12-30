"""
ASGI config for Hotel Management System.
Mounts FastAPI alongside Django.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

# Initialize Django ASGI application first
django_asgi_app = get_asgi_application()

# Import FastAPI app after Django is initialized
from api import app as fastapi_app


async def application(scope, receive, send):
    """
    ASGI application that routes requests between Django and FastAPI.
    
    - Requests to /api/* are handled by FastAPI
    - All other requests are handled by Django
    """
    if scope["type"] == "http":
        path = scope.get("path", "")
        
        # Route /api/* to FastAPI
        if path.startswith("/api"):
            await fastapi_app(scope, receive, send)
        else:
            await django_asgi_app(scope, receive, send)
    else:
        await django_asgi_app(scope, receive, send)
