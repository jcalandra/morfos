import numpy as np
from module_parameters import parameters
from Bio import pairwise2

quotient = parameters.QUOTIENT
threshold = parameters.TETA


def mean_pitches(obj_compared, actual_obj):
    print("obj_compared", obj_compared)
    print("actual_obj", actual_obj)
    mean_pitch_compared = np.mean(obj_compared)
    mean_pitch_actual = np.mean(actual_obj)
    sim_value = 1 - (abs(mean_pitch_compared - mean_pitch_actual)/127)
    print("sim_value", sim_value)
    if sim_value >= threshold:
        sim_digit_label = 1
    else:
        sim_digit_label = 0
    return sim_digit_label, sim_value

def alignement_pitch(string_compared, actual_string):
    alignment = -pow(10, 10)
    if len(actual_string) == 0:
        return 0, 0
    min_len = min(len(string_compared), len(actual_string))
    nw_align = pairwise2.align.globalxx(string_compared, actual_string)
    if len(nw_align) == 0:
        return 0, 0
    nw_alignment = nw_align[0][2]
    if nw_alignment > alignment:
        alignment = nw_alignment
    if min_len == 1:
        similarity = nw_alignment
    else:
        similarity = (alignment) / min_len
    sim_value = similarity
    if sim_value < 0:
        sim_value = 0
    if sim_value > 1:
        sim_value = 1
    if sim_value >= threshold:
        sim_digit_label = 1
    else:
        sim_digit_label = 0
    return sim_digit_label, sim_value

