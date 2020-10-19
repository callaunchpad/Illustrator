"""
Classes for defining a game instance
"""
from enum import Enum
# from .game_round import Round, Drawing
from .utils import Timer
import numpy as np

from .. import socketio

class Game:
  def __init__(self, id, socketio_instance, num_rounds=3, players=[], deck=["apple","banana","corn","dog"]):
    self.players = players
    self.state = GameState()
    self.deck = deck
    self.leaderboard = []     # list of ordered tuples
    self.num_rounds = num_rounds   # initialized by game creator
    self.curr_round = 1
    self.id = id
    self.game_round = None
    self.socketio_instance = socketio_instance

  def playGame(self):
    while self.curr_round != self.num_rounds:
      self.playRound()
    self.endGame()

  def endGame(self):
    self.showLeaderboard()
    self.state.status = 'ended'
    self.socketio_instance.emit("end_game", {"leaderboard": self.leaderboard}, room=self.id)
  
  def addPlayer(self, id):
    self.players.append(id)

  def playRound(self):
    self.game_round = Round(self)
    self.game_round.runRound()
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

class Round:
  def __init__(self, game):
    self.players_drawn = []
    self.players_copy = game.players.copy()
    self.game = game
    self.drawing = ""
    self.choice = ""
  
  def runRound(self):
    while len(self.players_drawn) < len(self.game.players):
      player = self.choosePlayer()
      self.next_drawing(player)
  
  def next_drawing(self, player):
    choice = self.chooseDrawing(player)
    self.drawing = Drawing(player,self,choice)
    self.drawing.draw()
    self.players_drawn.append(player)

  def choosePlayer(self):
    player = self.players_copy[0]   # choose player who hasn't drawn
    self.players_copy.remove(player)  # delete from possible players to draw
    return player    # return player object

  def chooseDrawing(self, player):
    options = np.random.choice(self.game.deck, 3, replace=False)
    # TODO remove those choices from self.deck

    self.choice = ""

    # TODO SOCKET: make choose_word REQUEST PLAYER TO CHOOSE from choices
    self.game.socketio_instance.emit("choose_word", {'options': list(options), 'player': player}, room=self.game.id)
    Timer.wait_time(3)
    return self.choice

"""
Class for defining a drawing
"""
class Drawing:
  def __init__(self, artist, round, choice, seconds=30):
    self.guesses = []  # incorrect guesses
    self.correct_players = []
    self.artist = artist
    self.choice = choice
    self.timer = Timer(seconds)
    self.round = round
  
  def draw(self):
    # Wait for 3 seconds before beginning the drawing
    Timer.wait_time(3)

    # Wait for 90 seconds as people guess, will later implement lowering / canceling 
    # clock as players get word and all players guess
    Timer.wait_time(90)
    while self.timer.check() or len(self.correct_players) < len(self.players):
      # self.showLeaderboard()


      # TODO start_draw stuff with socket responses