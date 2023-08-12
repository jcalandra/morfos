import class_signal
import class_object
from parameters import FORMAT

def compute_data_signal(path):
    return 0

def compute_data_vector(vector):
    return 0

def compute_data_symbol(name):
    nb_hop = len(name)
    obj_tab = []
    for i in range(nb_hop):
        new_rep = class_object.ObjRep()
        new_rep.init([], name[i], class_object.Descriptors())
        new_signal = []
        new_descriptors = class_object.Descriptors()
        #new_descriptors.init([["a"],["b"]],[["a"],["b"]])
        new_descriptors.init([[[1]],[[2,2],[2,2]]],[[[1]],[[2,2],[2,2]]])


        new_obj = class_object.Object()
        new_obj.update(new_rep.label, new_descriptors, new_signal, new_rep)
        obj_tab.append(new_obj)
    return obj_tab

def precompute_signal(pre_data):
    return pre_data

def precompute_vector(pre_data):
    return pre_data

def precompute_symbol(pre_data):
    return pre_data

def precompute_data(pre_data):
    if FORMAT == ".txt":
        data = precompute_symbol(pre_data)
    elif format == ".npy":
        data = precompute_vector(pre_data)
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