import os
from os import path
import sys
cwd = os.path.dirname(os.path.realpath(__file__))

import matplotlib.pyplot as plt
from matplotlib import image
import numpy as np
import time
import tensorflow as tf
import keras

# Read paths from gsutil ls output
paths = []
with open(path.join(cwd, 'names.txt'),'r') as f:
    for line in f.readlines():
        if "full" in line:
            continue
        paths.append(line.replace("\n",""))
paths = np.array(paths)

#Get Human-Readable names from paths
names = [path.split('/')[-1].replace('.npz','') for path in paths]

# load model
model = keras.models.load_model(path.join(cwd, 'mobilenet_beach.h5'))
def read(path):
	'''
	Reads in time series given the path to the time series txt data
	'''
	return open(path,'r').readlines()

def convert(series):
  '''
  Convert time series data into pairs of (x1,y1,x2,y2) strokes 
  '''
  xy_img = []
  for line in series:
    # line = eval(line)
    xy_img.append((line['x1'],-1 * line['y1'], line['x2'],-1 * line['y2'], line['penLifted']))
  return xy_img
    
def get_img(xy_img):
  '''
  Get an image to pass into ResNet from the strokes
  '''
  # i = 0
  # xs, ys = [], []
  # while i < len(xy_img):
  #   line = xy_img[i]
  #   penLifted = line[-1]
  #   while i < len(xy_img)-1 and not penLifted:
  #     xs.extend([line[0], line[2]])
  #     ys.extend([line[1], line[3]])
  #     i += 1
  #     line = xy_img[i]
  #     penLifted = line[-1]
  #   i += 1
  #   plt.plot(xs, ys)
  #   plt.axis('off')
  #   xs, ys = [], []
  for line in xy_img:
    plt.plot([line[0], line[2]],[line[1], line[3]])
    plt.axis('off')
  plt.savefig(path.join(cwd, 'temp.jpg'),facecolor='black')
  temp = image.imread(path.join(cwd, "temp.jpg"))
  plt.clf()
  plt.close()
  return temp

def pred(img, classes):
  '''
  Predict the class with the highest probability
  '''
  top_n = 23
  predictions = model.predict(np.array([img]))[0]
  print("model predictions: ", predictions)
  res = predictions.argsort()[-1*top_n:][::-1] # take top n predictions
  # res = classes[np.argmax(model.predict(np.array([img])))]
  return res
      
def classify(series):
  xy_img = convert(series)
  img = get_img(xy_img)
  res = pred(img, names)
  print("res is: ", res)
  return [int(idx) for idx in res] # numpy arrays and dtypes are not json serializable
