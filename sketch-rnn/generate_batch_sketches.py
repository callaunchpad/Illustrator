#!/usr/bin/env python3
"""
generate_batch_sketches.py generates 10 example sketches per class in the
experiments directory and outputs by each class as {class_name}.svg
"""
import argparse
from IPython.display import SVG, display
import json
import os
import svgwrite
from seq2seqVAE_train import *
from seq2seqVAE import sample
from utils import *

def draw_strokes(data, factor=0.2, svg_filename = '/tmp/sketch_rnn/svg/sample.svg'):
    if not os.path.exists(os.path.dirname(svg_filename)):
        os.makedirs(os.path.dirname(svg_filename))
    min_x, max_x, min_y, max_y = get_bounds(data, factor)
    dims = (50 + max_x - min_x, 50 + max_y - min_y)
    dwg = svgwrite.Drawing(svg_filename, size=dims)
    dwg.add(dwg.rect(insert=(0, 0), size=dims,fill='white'))
    lift_pen = 1
    abs_x = 25 - min_x 
    abs_y = 25 - min_y
    p = "M%s,%s " % (abs_x, abs_y)
    command = "m"
    for i in range(len(data)):
        if (lift_pen == 1):
            command = "m"
        elif (command != "l"):
            command = "l"
        else:
            command = ""
        x = float(data[i,0])/factor
        y = float(data[i,1])/factor
        lift_pen = data[i, 2]
        p += command+str(x)+","+str(y)+" "
    the_color = "black"
    stroke_width = 1
    dwg.add(dwg.path(p).stroke(the_color,stroke_width).fill("none"))
    dwg.save()
    return SVG(dwg.tostring())

# generate a 2D grid of many vector drawings
def make_grid_svg(s_list, grid_space=10.0, grid_space_x=16.0):
    def get_start_and_end(x):
        x = np.array(x)
        x = x[:, 0:2]
        x_start = x[0]
        x_end = x.sum(axis=0)
        x = x.cumsum(axis=0)
        x_max = x.max(axis=0)
        x_min = x.min(axis=0)
        center_loc = (x_max+x_min)*0.5
        return x_start-center_loc, x_end
    x_pos = 0.0
    y_pos = 0.0
    result = [[x_pos, y_pos, 1]]
    for sample in s_list:
        s = sample[0]
        grid_loc = sample[1]
        grid_y = grid_loc[0]*grid_space+grid_space*0.5
        grid_x = grid_loc[1]*grid_space_x+grid_space_x*0.5
        start_loc, delta_pos = get_start_and_end(s)
    
        loc_x = start_loc[0]
        loc_y = start_loc[1]
        new_x_pos = grid_x+loc_x
        new_y_pos = grid_y+loc_y
        result.append([new_x_pos-x_pos, new_y_pos-y_pos, 0])
    
        result += s.tolist()
        result[-1][2] = 1
        x_pos = new_x_pos+delta_pos[0]
        y_pos = new_y_pos+delta_pos[1]
    return np.array(result)

# Function for decoding a latent space factor into a sketch
def decode(seq2seq, model_params, z_input=None, draw_mode=True, temperature=0.1, factor=0.2):
    z = None
    if z_input is not None:
        z = z_input
    sample_strokes, m = sample(seq2seq, seq_len=model_params.max_seq_len, temperature=temperature, z=z)
    strokes = to_normal_strokes(sample_strokes)
    if draw_mode:
        draw_strokes(strokes, factor)
    return strokes

def draw_and_save_all(num_images_per_class): 
    """
    draw NUM_IMAGES_PER_CLASS number of sketches and saves it to ./generated_outputs
    """
    weights_fname = 'weights.hdf5'

    for class_name in os.listdir('experiments'):
        exp_dir = 'experiments/{0}'.format(class_name)
        with open(os.path.join(exp_dir,'logs', 'model_config.json'), 'r') as f:
            model_params = json.load(f)
        model_params = DotDict(model_params)   

        weights = os.path.join(exp_dir,'checkpoints',weights_fname) # checkpoint path
        seq2seq = Seq2seqModel(model_params)  # build model
        seq2seq.load_trained_weights(weights) # load checkpoint
        seq2seq.make_sampling_models()  # build sub models that are used to infuse inputs and probe values of intermediate layers

        stroke_list = []
        for i in range(num_images_per_class):
            out = np.expand_dims(np.random.randn(model_params.z_size),0)
            strokes = decode(seq2seq,model_params,out,draw_mode=False)
            stroke_list.append([strokes,[0, i]])
            bounds = get_bounds(strokes)
            
        stroke_grid = make_grid_svg(stroke_list)
        draw_strokes(stroke_grid, svg_filename="generated_sketch_outputs/{0}.svg".format(class_name))


if __name__ == "__main__":
    if not os.path.exists("generated_sketch_outputs"):
        os.makedirs("generated_sketch_outputs")

    draw_and_save_all(num_images_per_class=10)



