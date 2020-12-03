"""
Class for defining a bot player
"""
import sys
import aiohttp
import numpy as np
from os import path
cwd = path.dirname(path.realpath(__file__))
from .player import Player
# from ..sketch_rnn.sketch_output import get_sketch_dictionary
from ..sketch_rnn.uncond_sketch_output import get_sketch_dictionary

paths = []
with open(path.join(cwd, 'names.txt'),'r') as f:
    for line in f.readlines():
        if "full" in line:
            continue
        paths.append(line.replace("\n",""))
paths = np.array(paths)
#Get Human-Readable names from paths
names = [path.split('/')[-1].replace('.npz','') for path in paths]

class Bot(Player):
  def __init__(self, model, deck, username='bot'):
    super().__init__(username)
    self.model = model
    self.deck  = deck # list of words to choose from
    self.rankings = deck # words ranked by the model's output probabilities
    self.sid = 0

  async def classify(self, strokes):
    async with aiohttp.ClientSession() as session:
      body = {'strokes': strokes}
      async with session.post('http://0.0.0.0:8080/classify', json=body) as resp:
      #async with session.post('localhost:3000/classify', json=body) as resp:
        json = await resp.json()
        print(json)
        pred = json['pred']
    print("top 5 words are: ", names[pred[0]], names[pred[1]], names[pred[2]], names[pred[3]], names[pred[4]])
    return names[pred[0]]

  def generate(self, word):
    print('generating strokes')
    strokes = get_sketch_dictionary(word, use_dataset=False)
    return strokes




