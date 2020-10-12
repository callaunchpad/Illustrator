"""
Classes for defining a game instance
"""
from enum import Enum 
import random

class Game:
  def __init__(self, id, num_rounds=3):
    self.players = []
    self.state = GameState()
    self.deck = []
    self.leaderboard = []     # list of ordered tuples
    self.num_rounds = num_rounds   # initialized by game creator
    self.passed_rounds = 0
    self.id = id

  def playGame(self):
    while self.passed_rounds != self.num_rounds:
      playRound()
    endGame()

  def endGame():
    # TODO socket that shows leaderboard

    self.status = 'ended'

  def playRound(self):
    round = Round()
    round.runRound()
    self.passed_rounds += 1

class GameState: 
  def __init__(self):
    self.status = 'started'
  
class Round(Game):
  def __init__(self):
    self.players_drawn = []
    self.players_copy = players.copy()
  
  def runRound(self):
    while len(self.players_drawn) < len(self.players):
      player = choosePlayer()
      next_drawing(player)
  
  def next_drawing(self, player):
    choice = chooseDrawing(player)
    drawing = Drawing(player, choice)
    drawing.draw()

    self.players_drawn.append(player)

  def choosePlayer(self):
    player = self.players_copy[0]   # choose highest score who hasn't drawn
    del players_copy[0]   # delete from possible players to draw
    return player[1]    # return player object

  def chooseDrawing(self):
    choices = random.choices(self.deck, 3)
    # TODO SOCKET: choose_word REQUEST PLAYER TO CHOOSE from choices
    # return choice

class Drawing:
  def __init__(self, artist, choice):
    self.guesses = []  # incorrect guesses
    self.correct_players = []
    self.artist = artist
    self.choice = choice
  
  def draw(self):
    #start_draw

  
