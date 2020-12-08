import os
from os import path
import sys
cwd = os.path.dirname(os.path.realpath(__file__))

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
import json
from glob import glob
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import math

import keras
from keras.models import Sequential
from keras.layers import BatchNormalization, Conv1D, LSTM, Dense, Dropout
from keras.metrics import top_k_categorical_accuracy
# Read paths from gsutil ls output
paths = []
with open(path.join(cwd, 'names.txt'),'r') as f:
    for line in f.readlines():
        if "full" in line:
            continue
        paths.append(line.replace("\n",""))
paths = np.array(paths)

#Get Human-Readable names from paths
words = [path.split('/')[-1].replace('.npz','') for path in paths]
# load model. Have to build it cuz we needa replace all CuDNNRNNs with normal LSTMs
def build_model():
    stroke_read_model = Sequential()
    stroke_read_model.add(BatchNormalization(input_shape = (None,)+(388332, 100, 3)[2:]))
    stroke_read_model.add(Conv1D(48, (5,)))
    stroke_read_model.add(Dropout(0.3))
    stroke_read_model.add(Conv1D(64, (5,)))
    stroke_read_model.add(Dropout(0.3))
    stroke_read_model.add(Conv1D(96, (3,)))
    stroke_read_model.add(Dropout(0.3))
    stroke_read_model.add(LSTM(128, recurrent_activation='sigmoid', return_sequences = True))
    stroke_read_model.add(Dropout(0.3))
    stroke_read_model.add(LSTM(512, recurrent_activation='sigmoid', return_sequences = False))
    stroke_read_model.add(Dropout(0.3))
    stroke_read_model.add(Dense(128))
    stroke_read_model.add(Dropout(0.3))
    stroke_read_model.add(Dense(len(words), activation = 'softmax'))
    def top_5_accuracy(x,y): return top_k_categorical_accuracy(x,y, 5)
    stroke_read_model.load_weights(path.join(cwd, 'stroke_model.h5'))
    return stroke_read_model
TOP_N = 10
model = build_model()
def txt_to_strokes(series, preprocessed=True):
    stroke = np.array([[e['x1'] for e in series],[e['y1'] for e in series]])
    lifts = [0]

    for i,e in enumerate(series):
        if e['penLifted']:
            lifts.append(i)

    stroke = stroke * 256 / np.max(stroke)
    strokes = []
    for i in range(1, len(lifts)):
        strokes.append([stroke[0][lifts[i-1]+1:lifts[i]],stroke[1][lifts[i-1]+1:lifts[i]]])

    if preprocessed:
        for idx, (x_coord,y_coord) in enumerate(strokes):
            if len(x_coord)>1:  
                angle = math.atan2(y_coord[1] - y_coord[0],x_coord[1] - x_coord[0])
                dist = ((y_coord[1] - y_coord[0])**2 + (x_coord[1] - x_coord[0])**2)**0.5
                keep = np.ones(x_coord.shape,dtype=bool)

                for i in range(2, len(x_coord)):
                    temp = math.atan2(y_coord[i] - y_coord[i-1],x_coord[i] - x_coord[i-1])
                    cur_dist = ((y_coord[i] - y_coord[i-1])**2 + (x_coord[i] - x_coord[i-1])**2)**0.5
                    if abs(temp - angle) > np.pi/12 and dist + cur_dist > 20:
                        angle = temp
                        dist = cur_dist
                    else:
                        keep[i] = 0
                        dist += cur_dist
                strokes[idx] = [strokes[idx][0][keep],strokes[idx][1][keep]]
    return strokes
    
def drawing_to_array(in_drawing, max_length = 108):
    out_arr = np.zeros((max_length, 3), dtype = np.uint8) # x, y, indicator if it is a new stroke
    c_idx = 0
    for seg_label, (x_coord, y_coord) in enumerate(in_drawing):
        last_idx = min(c_idx + len(x_coord), max_length)
        seq_len = last_idx - c_idx
        out_arr[c_idx:last_idx, 0] = x_coord[:seq_len]
        out_arr[c_idx:last_idx, 1] = y_coord[:seq_len]
        out_arr[c_idx, 2] = 1 # indicate a new stroke
        c_idx = last_idx
        if last_idx>=max_length:
            break
    out_arr[:last_idx, 2] += 1
    return out_arr
      
def classify(series):
  arr = drawing_to_array(txt_to_strokes(series))  
  pred = model.predict(np.array([arr]))[0]
  print("model predictions: ", pred)
  res = pred.argsort()[-1*TOP_N:][::-1]
  return [int(idx) for idx in res] # numpy arrays and dtypes are not json serializable