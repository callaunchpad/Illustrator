"""
Classes for defining a game instance
"""
from enum import Enum
# from .game_round import Round, Drawing
from .utils import Timer
import eventlet
import numpy as np

from .. import socketio

class Game:
  def __init__(self, id, socketio_instance, num_rounds=3, players=[], deck=["apple","banana","corn","dog"]):
    self.players = players
    self.state = GameState()
    self.deck = deck
    self.leaderboard = {}     # list of ordered tuples
    self.num_rounds = num_rounds   # initialized by game creator
    self.curr_round = 1
    self.id = id
    self.game_round = None
    self.socketio_instance = socketio_instance

  async def playGame(self):
    print("STARTING GAME...")
    while self.curr_round != self.num_rounds:
      print('curr_round is: ', self.curr_round)
      await self.playRound()
    await self.endGame()

  async def endGame(self):
    print("ENDING GAME...")
    self.showLeaderboard()
    self.state.status = 'ended'
    await self.socketio_instance.emit("end_game", {"leaderboard": self.leaderboard}, room=self.id)
    self.curr_round = 1
    self.players = []
  
  def addPlayer(self, id):
    self.players.append(id)
    self.leaderboard[id] = 0

  async def playRound(self):
    print("STARTING ROUND" + str(self.curr_round))
    self.game_round = Round(self)
    await self.game_round.runRound()
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
    self.drawing = Drawing("",0,"")
    self.choice = ""
  
  async def runRound(self):
    while len(self.players_drawn) < len(self.game.players):
      player = self.choosePlayer()
      await self.next_drawing(player)
  
  async def next_drawing(self, player):
    choice = await self.chooseDrawing(player)
    print("THE CHOICE IS...." + choice)
    self.drawing = Drawing(player, self, choice, 30)
    print("WAITING FOR DRAWING, you have 30 seconds")
    await self.drawing.draw()
    self.players_drawn.append(player)

  def choosePlayer(self):
    player = self.players_copy[0]   # choose player who hasn't drawn
    self.players_copy.remove(player)  # delete from possible players to draw
    return player    # return player object
    
  async def chooseDrawing(self, player):
    options = np.random.choice(self.game.deck, 3, replace=False)
    # TODO remove those choices from self.deck

    self.choice = ""

    # TODO SOCKET: make choose_word REQUEST PLAYER TO CHOOSE from choices
    await self.game.socketio_instance.emit("choose_word", {'options': list(options), 'player': player}, room=player)
    print("CHOOSING WORD")
    await self.game.socketio_instance.sleep(5)
    if (len(self.choice) == 0):
      self.choice = np.random.choice(options)
      await self.game.socketio_instance.emit("close_word", room=player)
    print("word is: ", self.choice)
    return self.choice

"""
Class for defining a drawing
"""
class Drawing:
  def __init__(self, artist, game_round, choice, seconds=1):
    self.guesses = []  # incorrect guesses
    self.correct_players = []
    self.artist = artist
    self.choice = choice
    self.timer = Timer(seconds + 3)  # to account for later wait_time stall
    self.time_limit = 20
    self.game_round = game_round
  
  async def draw(self):
    # Wait for 3 seconds before beginning the drawing
    # Wait for x seconds as people guess, will later implement lowering / canceling 
    # clock as players get word and all players guess
    
    while self.timer.check() and len(self.correct_players) < len(self.game_round.game.players):
      # self.showLeaderboard()
      await self.game_round.game.socketio_instance.sleep(0)
      # TODO start_draw stuff with socket responses
    
    await self.game_round.game.socketio_instance.emit("show_leaderboard", {"leaderboard": self.game_round.game.leaderboard}, room=self.game_round.game.id)

  def checkGuess(self, player, guess):
    print("THE GUESS IS " + guess + "AND THE CORRECT ONE IS " + self.choice)
    if guess == self.choice and (player not in self.correct_players):
      self.correct_players.append(player)
      # TODO: have some score multiplier with the time?
      # add points to a player, maybe move to another method later
      self.game_round.game.leaderboard[player] += self.time_limit - self.timer.current_time()
      return True
    else:
      self.guesses.append(guess)
      return False