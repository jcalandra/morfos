import data_computing as dc
import math
import class_object
import numpy as np
from music21 import converter, corpus, instrument, midi, note, chord, pitch
from module_parameters.parameters import FORMAT, HOP_LENGTH, NOTE_MIN, NB_VALUES, MFCC_BIT, FFT_BIT, NB_SILENCE
from class_cdata import CData, ParsedElement, Elements


# signal

def dims_oracle(nb_values, s_tab):
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

def parse_signal(pre_data):
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
    input_data, dim = dims_oracle(NB_VALUES, s_tab)

    parsed_signal = ParsedElement()
    elements = Elements()
    elements.set_audio(audio)
    parsed_signal.set_elements(elements)
    parsed_signal.set_velocity(v_tab)
    parsed_signal.set_date([i for i in range(len(input_data))])
    parsed_signal.set_duration([1 for i in range(len(input_data))])
    parsed_signal.set_descriptors(input_data)
    parsed_signal.set_length(len(input_data))
    print("data_size", data_size)
    print("data_length", data_length)
    print("parsed_signal.length", parsed_signal.length)
    return parsed_signal, dim

def precompute_signal(pre_data):
    parsed_signal, dim = parse_signal(pre_data)

    cdata = CData()
    cdata.set_input_data(parsed_signal)
    cdata.set_dim(dim)
    cdata.set_type("signal")
    return cdata


def compute_data_signal(cdata):
    audio = cdata.input_data.elements.audio
    s_tab = cdata.input_data.descriptors
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

# vector

def parse_vector(pre_data):
    return pre_data

def precompute_vector(pre_data):
    return pre_data

def compute_data_vector(vector):
    return 0

# midi

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
    parsed_midi = ParsedElement()
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
    
    elements = Elements()
    elements.set_pitch(pitch)
    parsed_midi.set_elements(elements)
    parsed_midi.set_duration(duration)
    parsed_midi.set_descriptors(descriptors)
    parsed_midi.set_velocity(velocity)
    parsed_midi.set_date(date)
    parsed_midi.set_length(len(parsed_midi.elements.pitch))
    return parsed_midi

def precompute_midi(pre_data):
    parsed_midi = parse_midi(pre_data)
    audio = 0
    v_tab = parsed_midi.velocity
    dim = 1 

    cdata = CData()
    cdata.set_input_data(parsed_midi)
    cdata.set_dim(dim)
    cdata.set_type("midi")
    return cdata

def compute_data_midi(cdata):
    pitch = cdata.input_data.elements.pitch
    duration = cdata.input_data.duration
    date = cdata.input_data.date
    desc = cdata.input_data.descriptors

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

# symbol

def parse_symbol(pre_data):
    #tab[0] = symbols, tab[1] = velocity, tab[2] = date, tab[3] = duration, tab[4] = descriptors, TODO: put into file
    parsed_symbol = ParsedElement()
    elements = Elements()
    elements.set_symbol(pre_data[0])
    parsed_symbol.set_elements(elements)
    parsed_symbol.set_velocity(pre_data[1])
    parsed_symbol.set_date(pre_data[2])
    parsed_symbol.set_duration(pre_data[3])
    parsed_symbol.set_descriptors(pre_data[4])
    parsed_symbol.set_length(len(parsed_symbol.elements.symbol))
    if len(parsed_symbol.velocity) != parsed_symbol.length:
        parsed_symbol.set_velocity([1 for i in range(parsed_symbol.length)])
    if len(parsed_symbol.date) != parsed_symbol.length:
        parsed_symbol.set_date([i for i in range(parsed_symbol.length)])
    if len(parsed_symbol.duration) != parsed_symbol.length:
        parsed_symbol.set_duration([1 for i in range(parsed_symbol.length)])
    if len(parsed_symbol.descriptors) != parsed_symbol.length:
        parsed_symbol.set_descriptors([class_object.Descriptors() for i in range(parsed_symbol.length)])
        for i in range(parsed_symbol.length):
            parsed_symbol.descriptors[i].init([[[1,2,3]]],[[[1,2,3]]])
    return parsed_symbol

def precompute_symbol(pre_data):
    parsed_symbol = parse_symbol(pre_data)
    dim = 1
    cdata = CData()
    cdata.set_input_data(parsed_symbol)
    cdata.set_dim(dim)
    cdata.set_type("symbol")
    return cdata

def compute_data_symbol(cdata):
    name = cdata.input_data.elements.symbol
    duration = cdata.input_data.duration
    descriptors = cdata.input_data.descriptors
    print("name",name)
    print("duration", duration)
    print("desc", descriptors)

    length = cdata.input_data.length
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

# precompute and compute data

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