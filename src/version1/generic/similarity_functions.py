import math
from matplotlib.pyplot import *
import version1.parameters as prm

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
def diff_concordance(s_tab, id_hop_a, id_hop_b):
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
        cs = cs / square
    elif square_a == 0 and square_b == 0:
        cs = 1
    else:
        cs = 0
    return cs


def euclid_distance(s_tab, id_hop_a, id_hop_b):
    """ Compute the euclid distance. """
    n = len(s_tab[id_hop_a])
    e_distance = 0
    for k in range(n):
        e_distance = e_distance + (s_tab[id_hop_a][k] - s_tab[id_hop_b][k]) ** 2
    e_distance = math.sqrt(e_distance)
    if e_distance == 0:
        fcc = 1
    else:
        fcc = 1 / (e_distance + 1)
    return fcc


# FFT
def frequency_static_similarity_fft(s_tab, id_hop_a, id_hop_b):  # common energy
    """ Compute the similarity between frequencies according to the chosen method."""
    if DIFF_CONCORDANCE:
        cs = diff_concordance(s_tab, id_hop_a, id_hop_b)
    elif EUCLID_DISTANCE:
        cs = euclid_distance(s_tab, id_hop_a, id_hop_b)
    else:
        # concordance is chosen
        cs = diff_concordance(s_tab, id_hop_a, id_hop_b)
    return cs


# MFCC
def frequency_static_similarity_mfcc(s_tab, id_hop_a, id_hop_b):
    """ Compute the euclid distance between each mfcc of two different hops."""
    if DIFF_CONCORDANCE:
        cs = diff_concordance(s_tab, id_hop_a, id_hop_b)
    elif EUCLID_DISTANCE:
        cs = euclid_distance(s_tab, id_hop_a, id_hop_b)
    else:
        # euclid_distance is chosen
        cs = euclid_distance(s_tab, id_hop_a, id_hop_b)
    return cs


def frequency_static_similarity_cqt(s_tab, id_hop_a, id_hop_b):
    """ Compute the cosine similarity between each cqt of two different hops."""
    if DIFF_CONCORDANCE:
        cs = diff_concordance(s_tab, id_hop_a, id_hop_b)
    elif EUCLID_DISTANCE:
        cs = euclid_distance(s_tab, id_hop_a, id_hop_b)
    else:
        # concordance is chosen
        cs = diff_concordance(s_tab, id_hop_a, id_hop_b)
    return cs


def frequency_static_similarity(s_tab, id_hop_a, id_hop_b):
    """ Compute the cosine similarity between each cqt of two different hops."""
    if DIFF_CONCORDANCE:
        cs = diff_concordance(s_tab, id_hop_a, id_hop_b)
    elif EUCLID_DISTANCE:
        cs = euclid_distance(s_tab, id_hop_a, id_hop_b)
    else:
        # concordance is chosen
        cs = diff_concordance(s_tab, id_hop_a, id_hop_b)
    return cs


# ---------------------- DYNAMIC FUNCTIONS -----------------------


# Volume
def get_diff_volumes(v_tab, id_hop_a, id_hop_b):
    """ Compute the difference between the volumes of hop_a and hop_b."""
    diff = abs(v_tab[id_hop_a] - v_tab[id_hop_b])
    return diff


def volume_dynamic_dissimilarities(v_tab, id_hop_a, id_hop_b):
    """ Compute the volume evolution between (hop_a and hop_b) and (hop_a - 1 and hop_b - 1)."""
    diff_a = get_diff_volumes(v_tab, id_hop_a, id_hop_b)
    if id_hop_b == 0:
        vdd = diff_a
    else:
        diff_b = get_diff_volumes(v_tab, id_hop_a - 1, id_hop_b - 1)
        vdd = abs(diff_a - diff_b)
    return vdd


def volume_kullback_leibler(v_tab, id_hop_a, id_hop_b):
    """ Compute the ratio between the volumes of hop_a and hop_b."""
    kl = 0
    if v_tab[id_hop_b] > 0:
        d = v_tab[id_hop_a] / v_tab[id_hop_b]
    else:
        d = 0
    if d > 0:
        kl = kl + v_tab[id_hop_a] * math.log(d, 10)
    else:
        kl = 0
    return kl


# Spectrum
# FFT
def get_diff_frequencies_fft(s_tab, id_hop_a, id_hop_b):
    """ Get the differential frequency spectrum corresponding to the substraction of the coefficient of the spectrum at
    time t and t-1 for each frequency for each t"""
    s_length = len(s_tab[id_hop_a])
    ds_tab = [0 for i in range(s_length)]
    for j in range(1, s_length):
        ds_tab[j] = s_tab[id_hop_a][j] - s_tab[id_hop_b][j]
    return ds_tab


def frequency_dynamic_dissimilarity_fft2(s_tab, id_hop_a, id_hop_b):
    """ Get the dynamic dissimilarity for fft."""
    ds_tab = get_diff_frequencies_fft(s_tab, id_hop_a, id_hop_b)
    ds_length = len(ds_tab)
    ed = 0
    for j in range(ds_length):
        ed = ed + (ds_tab[j]) ** 2
    ed = math.sqrt(ed)
    return ed


def frequency_dynamic_dissimilarity_fft(s_tab, id_hop_a, id_hop_b):
    """ Get the dynamic dissimilarity for fft."""
    s_length = len(s_tab[id_hop_a])
    kl = 0
    for j in range(s_length):
        if s_tab[id_hop_b][j] > 0:
            d = s_tab[id_hop_a][j] / s_tab[id_hop_b][j]
        else:
            d = 0
        if d > 0:
            kl = kl + s_tab[id_hop_a][j] * math.log(d, 10)
        else:
            kl = 0
    return kl


# MFCC and CQT
def get_diff_frequencies_mfcc_cqt(s_tab, id_hop_a, id_hop_b):
    """ Get the differential frequency spectrum corresponding to the substraction of the coefficient of the spectrum at
    time t and t-1 for each frequency for each t"""
    s_length = len(s_tab)
    ds_tab = [0 for i in range(s_length)]
    for j in range(1, s_length):
        ds_tab[j] = s_tab[j][id_hop_a] - s_tab[j][id_hop_b]
    return ds_tab


def frequency_dynamic_dissimilarity_mfcc_cqt(s_tab, id_hop_a, id_hop_b):
    """ Get the dynamic dissimilarity for mfcc and cqt."""
    ds_tab = get_diff_frequencies_mfcc_cqt(s_tab, id_hop_a, id_hop_b)
    ds_length = len(ds_tab)
    ed = 0
    for j in range(ds_length):
        ed = ed + (ds_tab[j]) ** 2
    ed = math.sqrt(ed)
    return ed

# ---------------------- CIRCULAR FUNCTIONS ---------------------

# Volume

# Spectrum


# ============================================ COMPARISON ==============================================================

'''def true_mat(i_hop_a, i_hop_b, i_hop_c, j_mat, prev2_mat, s_tab):
    """ Return the closer object of i_hop_a between 'i_hop_b' and 'i_hop_c'."""
    fss = fss2 = 0
    if prm.processing=='signal' and FFT_BIT or prm.processing=='vectors':
        fss = frequency_static_similarity(s_tab, i_hop_a, i_hop_b)
        fss2 = frequency_static_similarity(s_tab, i_hop_a, i_hop_c)
    if prm.processing=='signal' and MFCC_BIT or CQT_BIT:
        s_tab_trans = s_tab.transpose()
        fss = frequency_static_similarity(s_tab_trans, i_hop_a, i_hop_b)
        fss2 = frequency_static_similarity(s_tab_trans, i_hop_a, i_hop_c)
    if max(fss2, fss) == fss:
        good_mat = j_mat
    else:
        good_mat = prev2_mat
    return good_mat'''


def true_mat(i_hop_a, i_hop_b, i_hop_c, j_mat, prev2_mat, s_tab):
    """ Return the closer object of i_hop_a between 'i_hop_b' and 'i_hop_c'."""
    fss = fss2 = 0
    if prm.processing=='signal' and FFT_BIT or prm.processing=='vectors':
        fss = frequency_static_similarity_fft(s_tab, i_hop_a, i_hop_b)
        fss2 = frequency_static_similarity_fft(s_tab, i_hop_a, i_hop_c)
    if prm.processing=='signal' and MFCC_BIT:
        s_tab_trans = s_tab.transpose()
        fss = frequency_static_similarity_mfcc(s_tab_trans, i_hop_a, i_hop_b)
        fss2 = frequency_static_similarity_mfcc(s_tab_trans, i_hop_a, i_hop_c)
    if prm.processing=='signal' and CQT_BIT:
        s_tab_trans = s_tab.transpose()
        fss = frequency_static_similarity_cqt(s_tab_trans, i_hop_a, i_hop_b)
        fss2 = frequency_static_similarity_cqt(s_tab_trans, i_hop_a, i_hop_c)
    if max(fss2, fss) == fss:
        good_mat = j_mat
    else:
        good_mat = prev2_mat
    return good_mat


def graph_comparison(i_hop, j_hop, path, teta, tab_comparison):
    """ Plot the curve of similarities between the actual object 'i_hop' and all objects heard before. These values are
    stored in 'tab_comparison'. Plot also the value of the similarity threshold along the axe."""
    figure(figsize=(12, 8))
    tab_frame = [i for i in range(len(tab_comparison))]
    plot(tab_frame, [teta for i in range(len(tab_comparison))])
    plot(tab_frame, tab_comparison)
    xlabel('Frame number')
    ylabel('Static similarity')
    name = path.split('/')[-1].split('.')[0]
    path_results = "../../results/teta/" + name + "/"
    path_name = name + "_actualframe" + str(i_hop) + "_similarframe" + str(j_hop)
    if j_hop == i_hop:
        j_hop = i_hop - 1
    title(name + " : Similarités statiques de la frame n°" + str(i_hop) +
          " avec les frames n°0 à n°" + str(j_hop))
    savefig(path_results + path_name)
    close()


def comparison(i_hop, teta, s_tab, v_tab, mat, path):
    """ Compare the actual object 'i_hop' with every object already seen before. If it is similar to an already seen
    object before i_hop, return the same material. Otherwise return -1."""
    tab_comparison = []
    fss = vss = 0
    if v_tab[i_hop] < AUDIBLE_THRESHOLD:
        return 0  # return silence material
    else:
        for j_hop in range(i_hop):
            if prm.processing=='signal' and FFT_BIT or prm.processing=='vectors':
                fss = frequency_static_similarity_fft(s_tab, i_hop, j_hop)
            elif prm.processing=='signal' and MFCC_BIT:
                s_tab_trans = s_tab.transpose()
                fss = frequency_static_similarity_mfcc(s_tab_trans, j_hop, i_hop)
            elif prm.processing=='signal' and CQT_BIT:
                s_tab_trans = s_tab.transpose()
                fss = frequency_static_similarity_cqt(s_tab_trans, j_hop, i_hop)
            # vss = volume_static_similarity(v_tab, i_hop, j_hop)
            static_similarity = fss
            tab_comparison.append(static_similarity)
            if static_similarity > teta and mat[j_hop] != 0:
                if GRAPH_COMPARISON:
                    graph_comparison(i_hop, j_hop, path, teta, tab_comparison)
                return mat[j_hop]
        if GRAPH_COMPARISON:
            graph_comparison(i_hop, i_hop, path, teta, tab_comparison)
    return -1


def dissimilarity(i_hop, s_tab, v_tab):
    """ Compute the dissimilarity between the frequencies of i_hop and i_hop - 1."""
    sdd = 0
    if prm.processing=='signal' and FFT_BIT or prm.processing=='vectors':
        if DIFF_FOURIER:
            sdd = frequency_dynamic_dissimilarity_fft2(s_tab, i_hop, i_hop - 1)
        elif DIFF_DYNAMIC:
            sdd = get_diff_volumes(v_tab, i_hop, i_hop - 1)
        else:
            sdd = get_diff_volumes(v_tab, i_hop, i_hop - 1)
    elif prm.processing=='signal' and (MFCC_BIT or CQT_BIT):
        if DIFF_FOURIER:
            sdd = frequency_dynamic_dissimilarity_mfcc_cqt(s_tab, i_hop, i_hop - 1)
        elif DIFF_DYNAMIC:
            sdd = get_diff_volumes(v_tab, i_hop, i_hop - 1)
        else:
            sdd = get_diff_volumes(v_tab, i_hop, i_hop - 1)

    if sdd > D_THRESHOLD:
        print(sdd, D_THRESHOLD)
        return 1
    return 0

# ========================================== REPRESENTANT IMPLEMENTATION ===============================================


def frequency_static_similarity_fft_rep(s_id_hop_a, m_id_hop_b):  # common energy
    """ Compute the cosine similarity of the frequencies between the frame
    id_hop_a and the frame id_hop_b."""
    square_a = square_b = cs = 0
    n = len(s_id_hop_a)
    # compute sqrt(sum(for j from 1 to s_length/ Aj^2)) between frame hop_i and frame hop_j
    for j in range(n):
        square_a = square_a + (s_id_hop_a[j]) ** 2
        square_b = square_b + (m_id_hop_b[j]) ** 2
    square = math.sqrt(square_a) * math.sqrt(square_b)
    # compute the cosine
    for j in range(1, n):
        cs = cs + s_id_hop_a[j] * m_id_hop_b[j]
    if square > 0:
        cs = cs / square
    elif square_a == 0 and square_b == 0:
        cs = 1
    else:
        cs = 0
    return cs


def true_mat_rep(m_i_hop_a, s_i_hop_b, m_i_hop_c, j_mat, prev2_mat):
    """ Return the closer class representative of m_i_hop_a between 's_i_hop_b' and 'm_i_hop_c'."""
    fss = fss2 = fun = 0
    if FFT_BIT:
        fss = frequency_static_similarity_fft_rep(m_i_hop_a, s_i_hop_b)
        fss2 = frequency_static_similarity_fft_rep(m_i_hop_a, m_i_hop_c)
    if max(fss2, fss) == fss:
        good_mat = j_mat
    else:
        good_mat = prev2_mat
    return good_mat


def comparison_rep(i_hop, teta, s_tab, v_tab, mat_rep):
    """ Compare the actual object 'i_hop' with a representant of every materials seen before. If it is similar to an
    class representative, return the same material. Otherwise return -1."""
    fss = 0
    audible_threshold = 0.005
    for j_hop in range(len(mat_rep)):
        if mat_rep[j_hop][1] != 0:
            if v_tab[i_hop] < audible_threshold:
                return 0  # return silence material
            else:
                if FFT_BIT:
                    fss = frequency_static_similarity_fft_rep(s_tab[i_hop], mat_rep[j_hop][0])
                elif MFCC_BIT:
                    # fss = frequency_static_similarity_mfcc(s_tab[i_hop], mat[j_hop][0])
                    print("not implemented")
                    return 0
                if fss > teta:
                    return j_hop
    return -1

