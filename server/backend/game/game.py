"""
Classes for defining a game instance
"""
from enum import Enum
from .utils import Timer
import random
from .. import socketio

class Game:
  def __init__(self, id, socketio_instance, num_rounds=3, players=[]):
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

class Round(Game):
  def __init__(self):
    self.players_drawn = []
    self.players_copy = self.players.copy()
  
  def runRound(self):
    while len(self.players_drawn) < len(self.players):
      player = self.choosePlayer()
      self.next_drawing(player)
  
  def next_drawing(self, player):
    choice = player.chooseDrawing()
    drawing = Drawing(player, choice)
    drawing.draw()
    self.players_drawn.append(player)

  def choosePlayer(self):
    player = self.players_copy[0]   # choose player who hasn't drawn
    del self.players_copy[0]   # delete from possible players to draw
    return player[1]    # return player object

  def chooseDrawing(self):
    choices = random.choices(self.deck, 3)
    # TODO remove those choices from self.deck

    # TODO SOCKET: choose_word REQUEST PLAYER TO CHOOSE from choices
    self.socketio_instance.emit("choose_word", {'data': choices}, room=self.id)
    return 'default'

"""
Class for defining a drawing
"""
class Drawing(Round):
  def __init__(self, artist, choice, seconds=30):
    self.guesses = []  # incorrect guesses
    self.correct_players = []
    self.artist = artist
    self.choice = choice
    self.timer = Timer(seconds)
  
  def draw(self):
    # Wait for 3 seconds before beginning the drawing
    Timer.wait_time(3)
    while self.timer.check() or len(self.correct_players) < len(self.players):
      self.showLeaderboard()

      # TODO start_draw stuff with socket responses