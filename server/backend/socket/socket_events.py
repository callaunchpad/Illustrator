"""
This file contains all the handlers for socket events. In other words, we define
the logic for how our server will respond to certain socket events triggered by the client
"""
# import tensorflow as tf
# from tensorflow import keras

import numpy as np
# from keras import backend as K

import socketio
from collections import defaultdict
# from ..sketch_rnn_keras.seq2seqVAE import Seq2seqModel, sample
# from ..sketch_rnn_keras.utils import DotDict, to_normal_strokes

from ..game.game import *
import json
import os
import time
dirname = os.path.dirname(__file__)

# initialize a socket instance
# change the * to the domain name of our client when applicable
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*', logger=True)
# need to do this to allow usage of tf 1
# tf.compat.v1.disable_eager_execution()

# dict for tracking active rooms
# maps room to list of players
ROOMS_GAMES = {'1': Game('1', sio, 4)}

"""
handler for when a user connects to the server
"""
# @sio.event
# def connect(sid, environ):
#   print('connected: ', sid)
@sio.on('connect')
def on_connect(sid, environ):
  """Create a game lobby"""
  print('connected:', sid)

"""
socket's response to receiving the drawer's canvas mouse movements
will broadcast the data back to all other users in the same room
also should append data that'll get processed into an image to feed into the classifier
"""
@sio.on('send_draw')
async def on_send_draw(sid, data):
  # print("SENDING DRAWING")
  room = data['roomId']
  game = ROOMS_GAMES[room]
  # print('SEND DRAW ROOM ID IS: ' + room)
  game.game_round.drawing.add_stroke(data)
  # with open("lisa.txt", "a") as myfile:
  #   myfile.write(str(data) + "\n")
  # TODO: alter game state for when drawing occurs
  await sio.emit('receive_draw', data, room=room)

"""
handler for when a player submits a guess
"""
@sio.on('send_guess')
async def on_send_guess(sid, data):
  print("SENDING GUESS")
  username = data['username']
  
  room = data['roomId']
  print('SEND GUESS ROOM ID IS: ' + room)
  guess = data['guess']
  game = ROOMS_GAMES[room]

  correct = game.game_round.drawing.checkGuess(sid, username, guess)
  if correct == 1:
    print("CORRECT GUESS!")
    await sio.emit('receive_answer', data, room=room)
  elif correct == 2:
    print("INCORRECT GUESS!")
    await sio.emit('receive_guess', data, room=room)
  elif correct == 3:
    await sio.emit('receive_own_guess', data, room=sid)
  elif correct == 4:
    await sio.emit('already_guessed', data, room=sid)

"""
handler for when a user creates a game
  data: username
"""
@sio.on('create_room')
async def on_create_room(sid, data):
  """Create a game lobby"""
  print("CREATING GAME SOCKET")
  print('data: ' + str(data))
  room = data['roomId']
  username = data['username']
  sio.enter_room(sid, room)

  ROOMS_GAMES[room] = Game(room, sio, 3) # need num_rounds from client? create game interface
  ROOMS_GAMES[room].addPlayer(sid, username)
  print("ROOMS_GAMES:")
  print(ROOMS_GAMES.items())
  print("ROOMS_GAMES Players List:")
  print(ROOMS_GAMES[room].players)
  await sio.emit('new_player_join', data, room=room)
  data['username'] = 'bot'
  await sio.emit('new_player_join', data, room=room)
  
"""
hanlder for when a user starts a game
"""
@sio.on('start_game')
async def on_start_game(sid, data):
  """Start a created game"""
  print("START GAME SOCKET")
  print("data: " + str(data))
  room = data["roomId"]
  print("EMITTING NEW_GAME")
  await sio.emit('new_game', data, room=sid)

"""
handler for when a user starts a game
"""
@sio.on('start')
async def on_start(sid, data):
  """Start a created game"""
  print("START SOCKET")
  print("data: " + str(data))
  room = data["roomId"]
  await ROOMS_GAMES[room].playGame()

"""
Handle when the artist clears the canvas. Basically just clear
the strokes the game is tracking for the classification model
"""
@sio.on('artist_cleared')
async def on_artist_clear(sid, data):
  room = data['roomId']
  game = ROOMS_GAMES[room]
  game.game_round.drawing.clear_strokes()

"""
handler for when a new user attempts to join a room
  data: username, room
"""
@sio.on('join')
async def on_join(sid, data):
  print("JOINING GAME SOCKET")
  print("data: " + str(data))
  room = data['roomId']
  username = data['username']
  sio.enter_room(sid, room)
  
  ROOMS_GAMES[room].addPlayer(sid, username)

  print("ROOMS_GAMES:")
  print(ROOMS_GAMES.items())
  print("ROOMS_GAMES Players List:")
  print(ROOMS_GAMES[room].players)
  await sio.emit('new_player_join', data, room=room)

"""
handler for when a user leaves the room they're in
"""
@sio.on('leave')
async def on_leave(sid, data):
  print('leaving... SOCKET')
  room = data['roomId']
  # ROOMS.pop(room)
  ROOMS_GAMES[room].removePlayer(sid)
  sio.leave_room(sid, room)
  await sio.emit('player_leave', data, room=room)

@sio.on("receive_word")
def on_receive_word(sid, data):
  room = data['roomId']
  word = data['word']
  print("RECEIVED_WORD SOCKET: ", word)

  game = ROOMS_GAMES[room]
  game.game_round.choice = word