"""
Class for defining a game round
"""
# from .game_class import Game
from .utils import Timer
import random

class Round(Game):
  def __init__(self):
    self.players_drawn = []
    self.players_copy = self.players.copy()
  
  def runRound(self):
    while len(self.players_drawn) < len(game.players):
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