"""
Class for defining a bot player
"""
from .player import Player

class Bot(Player):
  def __init__(self):
    super()
    self.model = None