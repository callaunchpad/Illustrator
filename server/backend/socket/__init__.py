from flask import Blueprint

socket_blueprint = Blueprint('socket_blueprint', __name__)

# all socket event handlers are defined in the socket_events.py file
from . import socket_events