import data_computing as dc
import math
import class_object
import numpy as np
from module_parameters.parameters import FORMAT, HOP_LENGTH, NOTE_MIN, NB_VALUES, MFCC_BIT, FFT_BIT, NB_SILENCE

def dims_oracle(nb_values, s_tab, v_tab):
    """Initialize an oracle with the given parameters."""
    if MFCC_BIT == 1:
        dim = nb_values - 1
        input_data = s_tab.transpose()
    elif FFT_BIT == 1:
        dim = len(s_tab[0])
        input_data = np.array(s_tab)
    else:
        dim = nb_values
        input_data = s_tab.transpose()

    if type(input_data) != np.ndarray or type(input_data[0]) != np.ndarray:
        input_data = np.array(input_data)
    if input_data.ndim != 2:
        input_data = np.expand_dims(input_data, axis=1)
    input_data = [input_data[i].tolist() for i in range(len(input_data))]
    s_tab = []
    s_tab.append(input_data)
    return s_tab, dim



def compute_data_signal(data):
    audio = data[0]
    s_tab = data[1]
    obj_tab = []
    nb_hop = len(s_tab[0])
    for i in range(nb_hop):
        stab_i = [[s_tab[0][i]]]
        new_rep = class_object.ObjRep()
        new_signal = [audio[i*HOP_LENGTH:(i+1)*HOP_LENGTH]]
        new_label = "a" # default label
        new_descriptors = class_object.Descriptors()
        new_descriptors.init(stab_i, stab_i)
        new_duration = HOP_LENGTH

        new_rep.init(new_signal, new_label, new_descriptors, new_duration)
        new_obj = class_object.Object()
        new_obj.update(new_signal, new_rep.label, new_descriptors, new_duration, new_rep)
        obj_tab.append(new_obj)
    return obj_tab

def compute_data_vector(vector):
    return 0

def compute_data_symbol(data):
    name = data[1]
    nb_hop = len(name)
    obj_tab = []
    for i in range(nb_hop):
        new_rep = class_object.ObjRep()
        new_rep.init([], name[i], class_object.Descriptors())
        new_signal = []
        new_descriptors = class_object.Descriptors()
        #new_descriptors.init([["a"],["b"]],[["a"],["b"]])
        new_descriptors.init([[[1,2,3]]],[[[1,2,3]]])

        new_obj = class_object.Object()
        new_obj.update(new_rep.label, new_descriptors, new_signal, new_rep)
        obj_tab.append(new_obj)
    return obj_tab

def compute_data_midi(data):
    return 0

def precompute_signal(pre_data):
    #ajouter la gestion des frames de silence
    audio, rate, data_size, data_length = dc.get_data(pre_data)
    audio_data = []
    for i in range(NB_SILENCE):
        audio_data.append(0)
    for i in range(len(audio)):
        audio_data.append(audio[i])
    data_size = int(data_size + NB_SILENCE)
    nb_hop = math.ceil(data_size/HOP_LENGTH)
    v_tab, s_tab = dc.get_descriptors(np.array(audio_data), rate, HOP_LENGTH, nb_hop, NB_VALUES, init=0,
                                      fmin=NOTE_MIN)
    input_data, dim = dims_oracle(NB_VALUES, s_tab, v_tab)
    return [audio, input_data, v_tab, dim]

def precompute_vector(pre_data):
    return pre_data

def parse_midi(pre_data):
    return pre_data

def precompute_midi(pre_data):
    audio = 0
    v_tab = [1 for i in range(len(pre_data))]
    dim = 1
    input_data = parse_midi(pre_data)
    return [audio, input_data, v_tab, dim]

def precompute_symbol(pre_data):
    audio = 0
    v_tab = [1 for i in range(len(pre_data))]
    dim = 1
    input_data = pre_data
    return [audio, input_data, v_tab, dim]

def precompute_data(pre_data):
    if FORMAT == ".txt":
        data = precompute_symbol(pre_data)
    elif format == ".npy":
        data = precompute_vector(pre_data)
    elif format == ".mid":
        data = precompute_midi(pre_data)
    else:
        data = precompute_signal(pre_data)
    return data

def compute_data(pre_data):
    if FORMAT == ".txt":
        data = compute_data_symbol(pre_data)
    elif format == ".npy":
        data = compute_data_vector(pre_data)
    else:
        data = compute_data_signal(pre_data)
    return data