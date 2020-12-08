"""
Class for defining a bot player
"""
import sys
import aiohttp
import asyncio
import numpy as np
from os import path
cwd = path.dirname(path.realpath(__file__))
from .player import Player
# from ..sketch_rnn.uncond_sketch_output import get_sketch_dictionary
from ..sketch_rnn.sketch_output import get_sketch_dictionary
paths = []
with open(path.join(cwd, 'names.txt'),'r') as f:
    for line in f.readlines():
        if "full" in line:
            continue
        paths.append(line.replace("\n",""))
paths = np.array(paths)
#Get Human-Readable names from paths
names = [path.split('/')[-1].replace('.npz','') for path in paths]

TOP_N = 10 # top n words to guess. The classify API call returns the top 10 most likely words
class Bot(Player):
  def __init__(self, model, deck, username='bot'):
    super().__init__(username)
    self.model = model
    self.deck  = deck # list of words to choose from
    self.rankings = deck # words ranked by the model's output probabilities
    self.sid = 0
    self.guesses = []
    self.guess_idx = 0

  async def classify(self, strokes):
    async with aiohttp.ClientSession() as session:
      body = {'strokes': strokes}
      async with session.post('http://0.0.0.0:8080/classify', json=body) as resp:
        json = await resp.json()
        pred = json['pred']
    # if predictions haven't changed since last inference, advance the guess_idx and guess the next most likely word
    if self.guesses == pred:
      self.guess_idx = min(self.guess_idx + 1, TOP_N - 1)
    else: # otherwise, reset the guessing index to be 0 and re assign the guessing queue
      self.guess_idx = 0
    self.guesses = pred
    return names[self.guesses[self.guess_idx]]

  def generate(self, word):
    print('generating strokes')
    strokes = get_sketch_dictionary(word, use_dataset=False)
    return strokes

  async def async_generate(self, word):
    print('async generating strokes')
    return await asyncio.coroutine(self.generate)(word)




