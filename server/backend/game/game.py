"""
Classes for defining a game instance
"""
from enum import Enum 

class Game:
  def __init__(self):
    self.players = []
    self.state = State()

class State: 
  def __init__(self):
    self.status = 'ended'