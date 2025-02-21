import math
from matplotlib.pyplot import *
from module_parameters import parameters as prm
import dtw

# In sim_function.py are computed distances in many ways.
# Functions that returns if two materials are the same or not are also provided as 'comparison functions'

MFCC_BIT = prm.MFCC_BIT
FFT_BIT = prm.FFT_BIT
CQT_BIT = prm.CQT_BIT
GRAPH_COMPARISON = prm.GRAPH_COMPARISON
AUDIBLE_THRESHOLD = prm.AUDIBLE_THRESHOLD
D_THRESHOLD = prm.D_THRESHOLD
NB_NOTES = prm.NB_NOTES

DIFF_CONCORDANCE = prm.DIFF_CONCORDANCE
EUCLID_DISTANCE = prm.EUCLID_DISTANCE
DIFF_FOURIER = prm.DIFF_FOURIER
DIFF_DYNAMIC = prm.DIFF_DYNAMIC

# ================================================= DISTANCES ==========================================================
# ---------------------- STATIC FUNCTIONS ------------------------


# Volume
def volume_static_similarity(v_tab, id_hop_a, id_hop_b):
    """ Compute the difference between the maximum volume of each hop."""
    diff = abs(v_tab[id_hop_a] - v_tab[id_hop_b]) / (2 * max(v_tab))
    vss = 1 - diff
    return vss


# Spectrum
def diff_concordance_stab(s_tab, id_hop_a, id_hop_b):
    """ Compute the cosine similarity of the frequencies between the frame
        id_hop_a and the frame id_hop_b."""
    square_a = square_b = cs = 0
    n = len(s_tab[id_hop_a])
    # compute sqrt(sum(for j from 1 to s_length/ Aj^2)) between frame hop_i and frame hop_j
    for j in range(n):
        a = s_tab[id_hop_a][j]
        b = s_tab[id_hop_b][j]
        square_a = square_a + a ** 2
        square_b = square_b + b ** 2
    square = math.sqrt(square_a) * math.sqrt(square_b)
    # compute the cosine
    for j in range(1, n):
        cs = cs + s_tab[id_hop_a][j] * s_tab[id_hop_b][j]
    if square > 0:
        sim_value = cs / square
    elif square_a == 0 and square_b == 0:
        sim_value = 1
    else:
        sim_value = 0
    if sim_value > prm.teta:
        sim_digit_label = 1
    else:
        sim_digit_label = 0
    return sim_digit_label, sim_value


def euclid_distance_stab(s_tab, id_hop_a, id_hop_b):
    """ Compute the euclid distance. """
    n = len(s_tab[id_hop_a])
    e_distance = 0
    for k in range(n):
        e_distance = e_distance + (s_tab[id_hop_a][k] - s_tab[id_hop_b][k]) ** 2
    e_distance = math.sqrt(e_distance)
    if e_distance == 0:
        sim_value = 1
    else:
        sim_value = 1 / (e_distance + 1)
    if sim_value > prm.teta:
        sim_digit_label = 1
    else:
        sim_digit_label = 0
    return sim_digit_label, sim_value

def diff_concordance(id_hop_a, id_hop_b):
    """ Compute the cosine similarity of the frequencies between the frame
        id_hop_a and the frame id_hop_b."""
    square_a = square_b = cs = 0
    n = len(id_hop_a)
    # compute sqrt(sum(for j from 1 to s_length/ Aj^2)) between frame hop_i and frame hop_j
    for j in range(n):
        a = id_hop_a[j]
        b = id_hop_b[j]
        square_a = square_a + a ** 2
        square_b = square_b + b ** 2
    square = math.sqrt(square_a) * math.sqrt(square_b)
    # compute the cosine
    for j in range(1, n):
        cs = cs + id_hop_a[j] * id_hop_b[j]
    if square > 0:
        sim_value = cs / square
    elif square_a == 0 and square_b == 0:
        sim_value = 1
    else:
        sim_value = 0
    if sim_value > prm.teta:
        sim_digit_label = 1
    else:
        sim_digit_label = 0
    return sim_digit_label, sim_value


def euclid_distance(id_hop_a, id_hop_b):
    """ Compute the euclid distance. """
    n = len(id_hop_a)
    e_distance = 0
    for k in range(n):
        e_distance = e_distance + (id_hop_a[k] - id_hop_b[k]) ** 2
    e_distance = math.sqrt(e_distance)
    if e_distance == 0:
        sim_value = 1
    else:
        sim_value = 1 / (e_distance + 1)
    if sim_value > prm.teta:
        sim_digit_label = 1
    else:
        sim_digit_label = 0
    return sim_digit_label, sim_value

def diff_dtw(id_hop_a, id_hop_b):
    """ Compute the dynamic time warping distance between two frames."""
    la = len(id_hop_a)
    lb = len(id_hop_b)
    vec_size = int(len(id_hop_a[0])*2/3)
    sim_value = 0
    #sim_values = []
    for k in range(vec_size):
        compared_lin = []
        actual_lin = []
        for l in range(la):
            compared_lin.append(id_hop_a[l][k])
        for l in range(lb):
            actual_lin.append(id_hop_b[l][k])

        ## Find the best match with the canonical recursion formula
        alignment = dtw.dtw(actual_lin, compared_lin, keep_internals=True)
        sim_val = 1/ (1 + alignment.distance/10000)
        print("distance", alignment.distance)
        print("sim_val", sim_val)
        
        sim_value += sim_val
    sim_value = sim_value/vec_size

    if sim_value > prm.teta:
        sim_digit_label = 1
    else:
        sim_digit_label = 0
    return sim_digit_label, sim_value
