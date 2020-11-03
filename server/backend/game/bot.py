"""
Class for defining a bot player
"""
from .player import Player
from ..sketch_rnn_keras.sketch_output import get_sketch_dictionary

class Bot(Player):
  def __init__(self, model, deck, username='bot'):
    super(username)
    self.model = None
    self.deck  = deck # list of words to choose from
    self.rankings = deck # words ranked by the model's output probabilities

  def classify(self, strokes):
    return 'dog'

  def generate(self, word):
    get_sketch_dictionary(word, use_dataset=False, draw_mode=False, weights_dir='./')
    return []



