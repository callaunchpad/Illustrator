"""
Classes for defining a game instance
"""
from enum import Enum
from .game_round import *
from .utils import Timer

from .. import socketio

class Game:
  def __init__(self, id, socketio_instance, num_rounds=3, players=[], deck=["apple","banana","corn","dog"]):
    self.players = players
    self.state = GameState()
    self.deck = []
    self.leaderboard = []     # list of ordered tuples
    self.num_rounds = num_rounds   # initialized by game creator
    self.curr_round = 1
    self.id = id
    self.socketio_instance = socketio_instance

  def playGame(self):
    while self.curr_round != self.num_rounds:
      self.playRound()
    self.endGame()

  def endGame(self):
    self.showLeaderboard()
    self.state.status = 'ended'
  
  def addPlayer(self, id):
    self.players.append(id)

  def playRound(self):
    game_round = Round()
    game_round.runRound()
    self.curr_round += 1
  
  def showLeaderboard(self):
    # TODO display leaderboard via socket
    None

"""
Class for defining a game state
"""
class GameState: 
  def __init__(self):
    self.status = 'started'

