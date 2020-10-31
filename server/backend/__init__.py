import socketio
from aiohttp import web
import aiohttp_cors
from .routes import routes
from .socket import socket_events

app = web.Application()
socket_events.sio.attach(app)
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
      allow_credentials=True,
      expose_headers="*",
      allow_headers="*",
    ),
})
app_routes = app.add_routes(routes.routes)
for route in app_routes:
  cors.add(route)