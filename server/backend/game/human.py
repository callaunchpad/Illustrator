"""
Class definition for human player
"""
from .player import Player

class Human(Player):
  def __init__(self, username, sid):
    super().__init__(username)
    self.sid = sid
  def __eq__(self, obj):
    return isinstance(obj, Human) and self.sid == obj.sid