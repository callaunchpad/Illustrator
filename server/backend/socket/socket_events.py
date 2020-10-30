"""
This file contains all the handlers for socket events. In other words, we define
the logic for how our server will respond to certain socket events triggered by the client
"""
import tensorflow as tf
from tensorflow import keras

import numpy as np
from keras import backend as K

from flask import session, request
from flask_socketio import emit, send, join_room, leave_room
from .. import socketio
from collections import defaultdict
from ..sketch_rnn_keras.seq2seqVAE import Seq2seqModel, sample
from ..sketch_rnn_keras.utils import DotDict, to_normal_strokes

from ..game.game import *
import json
import os
import time
dirname = os.path.dirname(__file__)
# need to do this to allow usage of tf 1
# tf.compat.v1.disable_eager_execution()

# dict for tracking active rooms
# maps room to list of players
ROOMS = defaultdict(list)

# ROOMS_GAMES = {}
ROOMS_GAMES = {'1': Game('1', socketio, 4)}

"""
hanlder for when a user connects to the server
"""
@socketio.on('connect')
def on_connect():
  """Create a game lobby"""
  print('connected:', request.sid)

"""
socket's response to receiving the drawer's canvas mouse movements
will broadcast the data back to all other users in the same room
also should append data that'll get processed into an image to feed into the classifier
"""
@socketio.on('send_draw')
def on_send_draw(data):
  # print("SENDING DRAWING")
  room = data['roomId']
  print(data)
  with open("circle.txt", "a") as myfile:
    myfile.write(str(data) + "\n")
  # TODO: alter game state for when drawing occurs
  emit('receive_draw', data, room=room)

"""
handler for when a player submits a guess
"""
@socketio.on('send_guess')
def on_send_guess(data):
  print("SENDING GUESS")
  room = data['roomId']
  guess = data['guess']

  game = ROOMS_GAMES[room]
  # TODO: alter game state for when guess occurs
  answer = "David"
  if guess == answer:
    game.game_round.drawing.correct_players.append(request.sid)  # will eventually switch to correctGuess method
    socketio.emit('receive_answer', data, room=room)

  else:
    socketio.emit('receive_guess', data, room=room)

"""
handler for when a user creates a game
  data: username
"""
@socketio.on('create_game')
def on_create_game(data):
  """Create a game lobby"""
  print("CREATING GAME SOCKET")
  print('data: ' + str(data))
  room = data['roomId'] # TODO generate random room ID
  # Use default join_room function: puts the user in a room
  join_room(room)

  # may not be necessary
  # ROOMS[room].append(request.sid)
  ROOMS_GAMES[room] = Game(room, socketio, data["num_rounds"], players=[request.sid]) # need num_rounds from client
  # print("ROOMS:")
  # print(ROOMS.items())
  print("ROOMS_GAMES:")
  print(ROOMS_GAMES.items())
  print("ROOMS_GAMES Players List:")
  print(ROOMS_GAMES[1].players)
  socketio.emit('join_room_msg', data, room=room)
  # emit("new_game", data, room=room)
  
"""
hanlder for when a user starts a game
"""
@socketio.on('start_game')
def on_start_game(data):
  """Start a created game"""
  print("START GAME SOCKET")
  print("data: " + str(data))
  room = data["roomId"]  # TODO: How to generate random room ID
  socketio.emit('new_game', data, room=room)
  # ROOMS_GAMES[room].playGame()
  # print("ROOMS_GAMES:")
  # print(ROOMS_GAMES.items())
  # print("ROOMS_GAMES Players List:")
  # print(ROOMS_GAMES['1'].players)
  # print("ROOMS_GAMES Round")
  # print(ROOMS_GAMES['1'].game_round)
  # print("ROOMS_GAMES Round Players_drawn")
  # print(ROOMS_GAMES['1'].game_round.players_drawn)
  # emit("new_game", data, room=room)

"""
handler for when a user starts a game
"""
@socketio.on('start')
def on_start_game(data):
  """Start a created game"""
  print("START SOCKET")
  print("data: " + str(data))
  room = data["roomId"]  # TODO: How to generate random room ID
  ROOMS_GAMES[room].playGame()

"""
handler for when a new user attempts to join a room
  data: username, room
"""
@socketio.on('join')
def on_join(data):
  print("JOINING GAME SOCKET")
  print("data: " + str(data))
  room = data['roomId']
  username = data['username']
  join_room(room)

  # may not be necessary
  # ROOMS[room].append(request.sid)
  
  ROOMS_GAMES[room].addPlayer(request.sid)
  # print("ROOMS:")
  # print(ROOMS.items())
  print("ROOMS_GAMES:")
  print(ROOMS_GAMES.items())
  print("ROOMS_GAMES Players List:")
  print(ROOMS_GAMES['1'].players)
  socketio.emit('new_player_join', data, room=room)
  # emit('new_player_join', {'roomId': room}, room=room)

"""
handler for when a user leaves the room they're in
"""
@socketio.on('leave')
def on_leave(data):
  print('leaving... SOCKET')
  username = data['username']
  room = data['roomId']
  # ROOMS.pop(room)

  ROOMS_GAMES[room].players.pop(request.sid)
  leave_room(room)
  socketio.emit('player_leave', data, room=room)
  # send(username + ' has left the room.', room=room)

@socketio.on("receive_word")
def on_receive_word(data):
  # username = data['username']

  # we will need these:
  room = data['roomId']
  word = data['word']
  print("RECEIVED_WORD SOCKET: ", word)

  game = ROOMS_GAMES[room]
  game.game_round.choice = word

"""
Function for decoding a latent space factor into a sketch
"""
def decode(seq2seq, model_params, z_input=None, draw_mode=False, temperature=0.1, factor=0.2):
    z = None
    if z_input is not None:
        z = z_input
    sample_strokes, m = sample(seq2seq, seq_len=model_params.max_seq_len, temperature=temperature, z=z)
    strokes = to_normal_strokes(sample_strokes)
    # if draw_mode:
    #     draw_strokes(strokes, factor)
    return strokes

"""
template for sampling from a really poorly trained sketchrnn for airplanes
"""
@socketio.on('test_sketch_rnn')
def on_test_sketch_rnn(data):
  room = data['roomId']
  # load the model hparams from the model_config json
  with open(os.path.join(dirname, 'model_weights/airplane_model_config.json'), 'r') as f:
    model_params = json.load(f)
  model_params = DotDict(model_params)
  # instantiate a seq2seq instance
  template_model = Seq2seqModel(model_params)
  hd5_path = os.path.join(dirname, 'model_weights/airplane.hdf5')
  template_model.load_trained_weights(hd5_path)
  # create sampling models for decoding/random sketch generation
  template_model.make_sampling_models()

  # sample a latent vector and feed into the decoder for random sketch generation
  random_latent_sample = np.expand_dims(np.random.randn(model_params.z_size),0)
  strokes = decode(template_model, model_params, z_input=random_latent_sample)
  print(strokes)

  # transform strokes list to correct drawing data format
  x, y = 250, 250
  for stroke in strokes:
    x += stroke[0]/.1
    y += stroke[1]/.1
    emit('receive_draw', {
      'x': x,
      'y': y,
      'pX': x,
      'pY': y,
      'strokeWidth': 4,
      'color': 'rgba(100%,0%,100%,0.5)'
    }, room=room)
    # stroke[2] is a binary indicator for if the pen was lifted or not (1 means lifted)
    if (stroke[2] == 1):
      time.sleep(.01)
  # need to clear the tf session between model inference calls for some reason
  K.clear_session()