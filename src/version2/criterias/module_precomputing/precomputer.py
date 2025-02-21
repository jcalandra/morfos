import data_computing as dc
import math
import class_object
import numpy as np
from music21 import converter, corpus, instrument, midi, note, chord, pitch
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
    length = len(s_tab[0])
    new_date = 0
    for i in range(length):
        stab_i_concat = [[s_tab[0][i]]]
        stab_i_mean = []
        for i in range(len(stab_i_concat)):
            stab_i_mean.append([])
            stab_i_mean[i].append([0 for _ in range(len(stab_i_concat[i][0]))])
            for j in range(len(stab_i_concat[i])):
                for k in range(len(stab_i_concat[i][j])):
                    stab_i_mean[i][0][k] += stab_i_concat[i][j][k]/len(stab_i_concat[0])
        new_rep = class_object.ObjRep()
        new_signal = [audio[i*HOP_LENGTH:(i+1)*HOP_LENGTH]]
        new_label = "a" # default label
        new_pitch = [0] # default pitch
        new_descriptors = class_object.Descriptors()
        new_descriptors.init(stab_i_concat, stab_i_mean)
        new_duration = int((HOP_LENGTH)/HOP_LENGTH)

        new_rep.init(new_signal, new_label, new_pitch, new_descriptors, new_duration, new_date)
        new_obj = class_object.Object()
        new_obj.update(new_signal, new_rep.label, new_pitch, new_descriptors, new_duration, new_date, new_rep)
        obj_tab.append(new_obj)
        new_date += new_duration
    return obj_tab

def compute_data_vector(vector):
    return 0

def compute_data_symbol(data):
    if len(data) != 4:
        raise ValueError("The data is not well formatted")
    name = data[1][0]
    print("name",name)
    duration = data[1][1]
    print("duratoin", duration)
    descriptors = data[1][2]
    print("desc", descriptors)
    if len(duration) != len(name):
        duration = [1 for i in range(len(name))]
    
    if len(descriptors) != len(name):
        descriptors = [class_object.Descriptors() for i in range(len(name))]
        for i in range(len(name)):
            descriptors[i].init([[[1,2,3]]],[[[1,2,3]]])

    length = len(name)
    obj_tab = []
    new_date = 0
    for i in range(length):
        new_signal = []
        new_label = name[i]
        new_pitch = [0]
        new_descriptors = class_object.Descriptors()
        new_descriptors = descriptors[i]
        new_duration = duration[i]

        new_rep = class_object.ObjRep()
        new_rep.init(new_signal, new_label, new_pitch, new_descriptors, duration[i], new_date)
        new_obj = class_object.Object()
        new_obj.update( new_signal, new_rep.label, new_pitch, new_descriptors, new_duration, new_date, new_rep)
        obj_tab.append(new_obj)
        new_date += new_duration
    return obj_tab

def compute_data_midi(data):
    pitch = data[1][0]
    duration = data[1][1]
    desc = data[1][2]
    date = data[1][4]

    descriptors = [class_object.Descriptors() for i in range(len(pitch))]
    length = len(pitch)
    obj_tab = []
    for i in range(length):
        new_signal = []
        new_label = "a" # default label
        new_pitch = [pitch[i]]
        descriptors[i].init(desc[i][0], desc[i][1])
        new_descriptors = class_object.Descriptors()
        new_descriptors = descriptors[i]
        new_duration = duration[i]
        new_date = date[i]

        new_rep = class_object.ObjRep()
        new_rep.init(new_signal, new_label, new_pitch, new_descriptors, new_duration, new_date)
        new_obj = class_object.Object()
        new_obj.update(new_signal, new_label, new_pitch, new_descriptors, new_duration, new_date, new_rep)
        obj_tab.append(new_obj)
    return obj_tab

def precompute_signal(pre_data):
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

def open_midi(midi_path, remove_drums):
    mf = midi.MidiFile()
    mf.open(midi_path)
    mf.read()
    mf.close()
    if (remove_drums):
        for i in range(len(mf.tracks)):
            mf.tracks[i].events = [ev for ev in mf.tracks[i].events if ev.channel != 10]          

    return midi.translate.midiFileToStream(mf)

def list_instruments(midi):
    partStream = midi.parts.stream()
    for p in partStream:
        aux = p
    return partStream

def extract_notes(midi_part):
    parent_element = []
    ret = []
    for nt in midi_part.flat.notes:        
        if isinstance(nt, note.Note):
            ret.append(max(0.0, nt.pitch.ps))
            parent_element.append(nt)
        elif isinstance(nt, chord.Chord):
            for pitch in nt.pitches:
                ret.append(max(0.0, pitch.ps))
                parent_element.append(nt)
    
    return ret, parent_element

def parse_midi(pre_data):
    #TODO: @jcalandra 30/01/25 - modeliser les silences
    midi_stream = open_midi(pre_data, 0)
    partStream = list_instruments(midi_stream)
    for instrument in partStream:
        y, parent_element = extract_notes(instrument.flat.notes)
        pitch = []
        duration = []
        descriptors = []
        velocity = []
        date = []
        for i in range(len(y)):
            pitch.append(y[i])
            dur = int(parent_element[i].duration.quarterLength*12)
            duration.append(dur)
            descriptors.append(([[[1,2,3]]],[[[1,2,3]]]))
            velocity.append(parent_element[i].volume.velocity)
            dat = int(parent_element[i].offset*12)
            date.append(dat)

    pre_data = [pitch, duration, descriptors, velocity, date]
    return pre_data

def precompute_midi(pre_data):
    input_data = parse_midi(pre_data)
    audio = 0
    v_tab = input_data[3]
    dim = 1 
    return [audio, input_data, v_tab, dim]

def precompute_symbol(pre_data):
    #tab[0] = symbols, tab[1] = duration, tab[2] = descriptors, tab[3] = velocity
    audio = 0
    if len(pre_data[3]) != len(pre_data[0]):
        pre_data[3] = [1 for i in range(len(pre_data[0]))]
    v_tab = pre_data[3]
    dim = 1
    input_data = pre_data
    return [audio, input_data, v_tab, dim]

def precompute_data(pre_data):
    if FORMAT == ".txt":
        data = precompute_symbol(pre_data)
    elif FORMAT == ".npy":
        data = precompute_vector(pre_data)
    elif FORMAT == ".mid":
        data = precompute_midi(pre_data)
    else:
        data = precompute_signal(pre_data)
    return data

def compute_data(pre_data):
    if FORMAT == ".txt":
        data = compute_data_symbol(pre_data)
    elif format == ".npy":
        data = compute_data_vector(pre_data)
    elif FORMAT == ".mid":
        data = compute_data_midi(pre_data)
    else:
        data = compute_data_signal(pre_data)
    return data