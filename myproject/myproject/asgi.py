import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Vercel serverless cannot run Channels/WebSockets (needs Redis).
if os.environ.get('VERCEL'):
    application = get_asgi_application()
else:
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    import chatbot.routing

    application = ProtocolTypeRouter({
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                chatbot.routing.websocket_urlpatterns
            )
        ),
    })