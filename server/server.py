# python stuff
import tensorflow as tf
from flask import Flask
from flask_socketio import SocketIO, join_room, emit, send
from flask_cors import CORS

app = Flask(__name__)

# gives cross origin access to all API routes
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# gives cross origin access to all sockets
socketio = SocketIO(app, cors_allowed_origins="*") 
ROOMS = {} # dict to track active rooms

@app.route('/', methods=['GET'])
def test():
  
  return {
    'test': True
  }

if __name__ == '__main__':
  socketio.run(app, debug=True)

@socketio.on('connect')
def on_connect():
    """Create a game lobby"""
    print('connected aowi;ejfo;iawjefo;iaweofaw;efji!')
    # print('created')
    # gm = "this is a game object"
    # roomId = 1 
    # ROOMS[roomId] = gm
    # join_room(roomId)
    # emit('join_room', {'room': roomId})

@socketio.on('send_draw')
def on_send_draw(data):
  print(data)
  emit('receive_draw', data, broadcast=True)

# @socketio.on('create')
# def on_create(data):
#     """Create a game lobby"""
#     print('created')
#     gm = "this is a game object"
#     roomId = 1 
#     ROOMS[roomId] = gm
#     join_room(roomId)
#     emit('join_room', {'room': roomId})