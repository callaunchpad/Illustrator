"""
Class for defining a bot player
"""
import sys
from os import path
from .player import Player
from ..sketch_rnn.sketch_output import get_sketch_dictionary
# cwd = path.dirname(path.realpath(__file__))
# sys.path.append(path.join('..', cwd, 'sketch-rnn'))
# from sketch_rnn import get_sketch_dictionary

class Bot(Player):
  def __init__(self, model, deck, username='bot'):
    super().__init__(username)
    self.model = model
    self.deck  = deck # list of words to choose from
    self.rankings = deck # words ranked by the model's output probabilities

  def classify(self, strokes):
    print('classifying sketch')
    return 'apple'

  def generate(self, word):
    print('generating strokes')
    strokes = get_sketch_dictionary(word, use_dataset=False, draw_mode=False)
    return strokes




