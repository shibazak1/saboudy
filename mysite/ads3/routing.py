from django.urls import re_path
from . import consumers




websocket_urlpatterns = [
    re_path(r'ws/track/(?P<order_id>\w+)/$', consumers.DriverTrackingConsumer.as_asgi()),
]
