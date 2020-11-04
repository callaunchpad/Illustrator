import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib import image
# import keras
import tensorflow.keras as keras
# import tensorflow as tf
import time

# Read paths from gsutil ls output
paths = []
with open('names.txt','r') as f:
    for line in f.readlines():
        if "full" in line:
            continue
        paths.append(line.replace("\n",""))
paths = np.array(paths)

#Get Human-Readable names from paths
names = [path.split('/')[-1].replace('.npz','') for path in paths]

# Load Model
model = keras.models.load_model('45.h5')

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
    temp = eval(line)
    xy_img.append((temp['x1'],-1 * temp['y1'],temp['x2'],-1 * temp['y2']))
  return xy_img
    
def get_img(xy_img):
  '''
  Get an image to pass into ResNet from the strokes
  '''
  for line in xy_img:
    plt.plot([line[0], line[2]],[line[1], line[3]])
    plt.axis('off')
    plt.savefig('temp.jpg',facecolor='black')
    temp = image.imread("temp.jpg")
    plt.clf()
    plt.close()
  return temp

def pred(img, model, classes):
  '''
  Predict the class with the highest probability
  '''
  return classes[np.argmax(model.predict(np.array([img])))]
      
series = read('airplane.txt')
xy_img = convert(series)
img = get_img(xy_img)

pred(img, model, names)