import tensorflow as tf
from flask import Flask
from flask_socketio import SocketIO, join_room, emit, send
from flask_cors import CORS

app = Flask(__name__)

# gives cross origin access to all API routes
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# gives cross origin access to all sockets
socketio = SocketIO(app, cors_allowed_origins="*", async_handlers=True)

from .socket import socket_blueprint
from .routes import routes_blueprint
app.register_blueprint(socket_blueprint)
app.register_blueprint(routes_blueprint)