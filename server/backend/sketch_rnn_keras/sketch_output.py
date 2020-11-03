#!/usr/bin/python3
import numpy as np
import os
from os import path
import copy
from utils import *

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from seq2seqVAE_train import *
import seq2seqVAE as sketch_rnn_model
from seq2seqVAE import sample

cwd = os.path.dirname(os.path.realpath(__file__))
# Set GPU affinity
# os.environ["CUDA_VISIBLE_DEVICES"]="4"

def generate_strokes_dictionary(strokes,factor=0.2):
    curr_pen_pos=[250,250]
    trans_x = []
    trans_y = []

    for x,y,p in strokes:
        curr_pen_pos[0] = curr_pen_pos[0]+(x/factor)
        curr_pen_pos[1] = curr_pen_pos[1]+(y/factor)
        trans_x.append(curr_pen_pos[0])
        trans_y.append(curr_pen_pos[1])

    res = []
    curr_x = 0
    curr_y = 0
    for i in range(len(trans_x)-1):
        curr_x = trans_x[i]
        curr_y = trans_y[i]

        next_x = trans_x[i+1]
        next_y = trans_y[i+1]
        pen_lift = int(strokes[i][2])

        res.append({'x1': curr_x, 'y1': curr_y, 'x2': next_x, 'y2': next_y, 'color': 'rgba(100%,0%,100%,0.5)', 'penLifted': pen_lift, 'strokeWidth': 4, 'roomId': '1'})

    last_x = trans_x[len(trans_x)-1]
    last_y = trans_y[len(trans_y)-1]
    last_pen_lift = int(strokes[len(strokes)-1][2])

    res.append({'x1': curr_x, 'y1': curr_y, 'x2': last_x, 'y2': last_y, 'color': 'rgba(100%,0%,100%,0.5)', 'penLifted': last_pen_lift, 'strokeWidth': 4, 'roomId': '1'})
    return res


def get_sketch_dictionary(class_name, use_dataset=False, draw_mode=True, model_dir=path.join('..', cwd, 'sketch_rnn')):
    """
    return sketch dictionary given a class name
    encode/decode from https://github.com/eyalzk/sketch_rnn_keras
    
    ARGS:
    * class_name: the name of the class to sketch
    * use_dataset: should I use the dataset to draw the image? This ignores the model (default: False)
      CSUA Latte's dataset directory: /dataset/sketch-rnn, see below
    * draw_mode: should I draw a copy of the sketch to the 'output/' folder? (default: True)
    """

    # Data directory on CSUA latte for grabbing datasets
    data_dir  = '/datasets/sketch-rnn'

    # Checkpoint file name (assumed in checkpoints folder within exp_dir)
    weights_fname = 'weights.hdf5'
    # Path to the experiment directory that was created during training
    class_dir = path.join(model_dir, 'experiments/{}'.format(class_name))

    if not path.exists(class_dir):
      raise ValueError("class name does not exist.")
    # model_folder = path.join(model_dir, class_name)
    # if not os.path.exists(model_folder):
    #   raise ValueError("class name does not exist.")

    config_path = path.join(class_dir, 'logs', 'model_config.json')
    with open(config_path, 'r') as f:
        model_params = json.load(f)
    model_params = DotDict(model_params)

    weights = path.join(class_dir,'checkpoints',weights_fname) # checkpoint path
    seq2seq = Seq2seqModel(model_params)  # build model
    seq2seq.load_trained_weights(weights) # load checkpoint
    seq2seq.make_sampling_models()  # build sub models that are used to infuse inputs and probe values of intermediate layers

    # Function for encoding input and retrieving latent vector
    def encode(input_strokes):
        strokes = to_big_strokes(input_strokes, max_len=model_params['max_seq_len']-1).tolist()
        strokes.insert(0, [0, 0, 1, 0, 0])
        seq_len = [len(input_strokes)]
        strokes = np.expand_dims(strokes, axis=0)
        return seq2seq.sample_models['encoder_model'].predict(strokes)

    # Function for decoding a latent space factor into a sketch
    def decode(z_input=None, temperature=0.1, factor=0.2):
        z = None
        if z_input is not None:
            z = z_input
        sample_strokes, m = sample(seq2seq, seq_len=model_params.max_seq_len, temperature=temperature, z=z)
        strokes = to_normal_strokes(sample_strokes)
        return strokes


    if use_dataset:
        # using dataset, will load dataset
        [train_set, valid_set, test_set, hps_model] = load_dataset(data_dir, model_params)
        stroke = test_set.random_sample()
        z = encode(stroke)
        strokes = decode(z, temperature=0.5) # convert z back to drawing at temperature of 0.5
    else:
        #use trained model instead
        model_z = np.expand_dims(np.random.randn(model_params.z_size),0)
        strokes = decode(model_z)
    
    strokes_dictionary = generate_strokes_dictionary(strokes,factor=0.05)

    if draw_mode:
        # set canvas size
        plt.figure(figsize=(8,8))
        plt.ylim(ymax = 0, ymin = 500)
        plt.xlim(xmax = 500, xmin = 0)

        # draw output
        for d in strokes_dictionary:
            x1 = d['x1']
            x2 = d['x2']
            y1 = d['y1']
            y2 = d['y2']
            p = d['penLifted']
            if not p:
                #plt.plot([x1, y1], [x2, y2], 'k', lw=2)
                plt.annotate("",
                      xy=(x1, y1), xycoords='data',
                      xytext=(x2, y2), textcoords='data',
                      arrowprops=dict(arrowstyle="-",
                                      edgecolor = "red",
                                      linewidth=3,
                                      alpha=0.65,
                                      connectionstyle="arc3,rad=0."),)
        plt.savefig("output/{}.jpg".format(class_name))

    print("Sketch of {} saved to output/{}.jpg".format(class_name,class_name))
    return strokes_dictionary