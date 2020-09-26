"""
Classes for defining a game instance
"""
from enum import Enum 

class Game:
  def __init__(self):
    self.players = []
    self.state = GameState()

class GameState: 
  def __init__(self):
    self.status = 'ended'