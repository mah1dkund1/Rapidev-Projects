import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from status.consumers import TerminalConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE' , 'config.settings')

application = ProtocolTypeRouter({

# this handles https reqs normally
"http": get_asgi_application(),

# this handles permanent websocket connections
"websocket": URLRouter([
    path("ws/terminal-stream/", TerminalConsumer.as_asgi()),
]),

})