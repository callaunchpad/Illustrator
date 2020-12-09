"""
This file contains all the handlers for socket events. In other words, we define
the logic for how our server will respond to certain socket events triggered by the client
"""
import os
import json
import time
import socketio
import numpy as np
from ..game.game import *
from ..globals import ROOMS_GAMES, PlAYER_TO_GAME, ROOM_USERNAMES
dirname = os.path.dirname(__file__)

# initialize a socket instance
# change the * to the domain name of our client when applicable
sio = socketio.AsyncServer(async_mode='aiohttp', cors_allowed_origins='*', logger=True)
# need to do this to allow usage of tf 1
# tf.compat.v1.disable_eager_execution()

"""
handler for when a user connects to the server
"""
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

  PlAYER_TO_GAME[sid] = room
  ROOMS_GAMES[room] = Game(room, sio, 3) # need num_rounds from client? create game interface
  ROOM_USERNAMES[room].add(username)
  ROOM_USERNAMES[room].add('bot') # don't forget to add bot's username!
  await ROOMS_GAMES[room].addPlayer(sid, username)
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
  await game.game_round.drawing.clear_strokes()

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
  PlAYER_TO_GAME[sid] = room
  ROOM_USERNAMES[room].add(username)
  await ROOMS_GAMES[room].addPlayer(sid, username)

  print("ROOMS_GAMES:")
  print(ROOMS_GAMES.items())
  print("ROOMS_GAMES Players List:")
  print(ROOMS_GAMES[room].players)
  await sio.emit('new_player_join', data, room=room)

"""
Handler for when the client chooses a word to draw
"""
@sio.on("receive_word")
def on_receive_word(sid, data):
  room = data['roomId']
  word = data['word']
  game = ROOMS_GAMES[room]
  game.game_round.choice = word

"""
handler for when a user leaves the room they're in. Same logic as disconnect
"""
@sio.on('leave')
async def on_leave(sid, data):
  print('leaving...')
  # don't do anything if player doesnt exist in this mapping. 
  # this happens if the client opens the app but doesn't actually join or create a game
  if (not PlAYER_TO_GAME.get(sid, False)):
    return
  game_id = PlAYER_TO_GAME[sid]
  # remove this player from the player_to_game map
  del PlAYER_TO_GAME[sid]
  game = ROOMS_GAMES[game_id]
  # remove this player's username from the set of usernames in this room
  for p in game.players:
    if p.sid == sid:
      ROOM_USERNAMES[game_id].remove(p.username)
      break
  # remove this player from the game they were in
  await game.removePlayer(sid)
  # destroy the game if only the bot remains
  if len(game.players) <= 1:
    del ROOMS_GAMES[game_id]
"""
handler for when a user disconnects. This happens when the tab closes, or they go back
to the home page, or they refresh
"""
@sio.on("disconnect")
async def disconnect(sid):
  print('disconnected: ', sid)
  # don't do anything if player doesnt exist in this mapping. 
  # this happens if the client opens the app but doesn't actually join or create a game
  if (not PlAYER_TO_GAME.get(sid, False)):
    return
  game_id = PlAYER_TO_GAME[sid]
  # remove this player from the player_to_game map
  del PlAYER_TO_GAME[sid]
  game = ROOMS_GAMES[game_id]
  # remove this player's username from the set of usernames in this room
  for p in game.players:
    if p.sid == sid:
      ROOM_USERNAMES[game_id].remove(p.username)
      break
  # remove this player from the game they were in
  await game.removePlayer(sid)
  # destroy the game if only the bot remains
  if len(game.players) <= 1:
    del ROOMS_GAMES[game_id]
