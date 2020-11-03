"""
Class for defining a player. Superclass of bot and human players
"""
class Player:
  def __init__(self, username):
    self.username = username
  def __eq__(self, obj):
    return isinstance(obj, Player) and obj.username == self.username
