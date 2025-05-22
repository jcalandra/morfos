import parameters as prm
import class_similarity_computation as csc
import math

RULE_1 = prm.DIFF_FOURIER
RULE_2 = prm.DIFF_DYNAMIC


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
def get_diff_frequencies_fft(id_hop_a, id_hop_b):
    """ Get the differential frequency spectrum corresponding to the substraction of the coefficient of the spectrum at
    time t and t-1 for each frequency for each t"""
    s_length = len(id_hop_a)
    ds_tab = [0 for i in range(s_length)]
    for j in range(1, s_length):
        ds_tab[j] = id_hop_a[j] - id_hop_b[j]
    return ds_tab


def frequency_dynamic_dissimilarity_fft2(id_hop_a, id_hop_b):
    """ Get the dynamic dissimilarity for fft."""
    ds_tab = get_diff_frequencies_fft(id_hop_a, id_hop_b)
    ds_length = len(ds_tab)
    ed = 0
    for j in range(ds_length):
        ed = ed + (ds_tab[j]) ** 2
    ed = math.sqrt(ed)
    return ed


def frequency_dynamic_dissimilarity_fft(id_hop_a, id_hop_b):
    """ Get the dynamic dissimilarity for fft."""
    s_length = len(id_hop_a)
    kl = 0
    for j in range(s_length):
        if id_hop_b[j] > 0:
            d = id_hop_a[j] / id_hop_b[j]
        else:
            d = 0
        if d > 0:
            kl = kl + id_hop_a[j] * math.log(d, 10)
        else:
            kl = 0
    return kl


# MFCC and CQT
def get_diff_frequencies_mfcc_cqt(id_hop_a, id_hop_b):
    """ Get the differential frequency spectrum corresponding to the substraction of the coefficient of the spectrum at
    time t and t-1 for each frequency for each t"""
    s_length = len(id_hop_a)
    ds_tab = [0 for i in range(s_length)]
    for j in range(1, s_length):
        ds_tab[j] = id_hop_a[j] - id_hop_b[j]
    return ds_tab


def frequency_dynamic_dissimilarity_mfcc_cqt(id_hop_a, id_hop_b):
    """ Get the dynamic dissimilarity for mfcc and cqt."""
    ds_tab = get_diff_frequencies_mfcc_cqt(id_hop_a, id_hop_b)
    ds_length = len(ds_tab)
    ed = 0
    for j in range(ds_length):
        ed = ed + (ds_tab[j]) ** 2
    ed = math.sqrt(ed)
    return ed



def rule1_dissimilarity(ms_oracle, level):
    """ Compute the dissimilarity between the frequencies of i_hop and i_hop - 1."""
    #v_tab = ms_oracle.levels[level].volume
    actual_ind = ms_oracle.levels[level].voices[0].actual_char_ind
    if actual_ind > 0 and len(ms_oracle.levels[level].voices[0].objects) > actual_ind:
        actual_obj = ms_oracle.levels[level].voices[0].objects[actual_ind].extNotes[0].note.descriptors.mean_descriptors[0][0]
        prec_obj = ms_oracle.levels[level].voices[0].objects[actual_ind - 1].extNotes[0].note.descriptors.mean_descriptors[0][0]
        sdd = 0
        if prm.processing=='signal' and prm.FFT_BIT or prm.processing=='vectors':
            if prm.DIFF_FOURIER:
                sdd = frequency_dynamic_dissimilarity_fft2(actual_obj, prec_obj)
            #elif prm.DIFF_DYNAMIC:
            #    sdd = get_diff_volumes(v_tab, actual_ind, actual_ind - 1)
            #else:
            #    sdd = get_diff_volumes(v_tab, actual_ind, actual_ind - 1)
        elif prm.processing=='signal' and (prm.MFCC_BIT or prm.CQT_BIT):
            if prm.DIFF_FOURIER:
                sdd = frequency_dynamic_dissimilarity_mfcc_cqt(actual_obj, prec_obj)
            #elif prm.DIFF_DYNAMIC:
            #    sdd = get_diff_volumes(v_tab, actual_ind, actual_ind - 1)
            #else:
            #    sdd = get_diff_volumes(v_tab, actual_ind, actual_ind - 1)
        if sdd > prm.D_THRESHOLD:
            return 1
    return 0

def rule2_isolated_object(ms_oracle, level):
    """ Don't segment if the concatenate object is of size 1."""
    if len(ms_oracle.levels[level].concat_obj.extConcatNote.concatNote.concat_labels) > 1:
        return 1
    return 0

#TODO: change label by descriptors csc.compute_signal_similarity
def rule_3a_repetition_paradigm_noseg(ms_oracle, level):
    concat_obj = ms_oracle.levels[level].concat_obj.extConcatNote.concatNote.concat_labels
    actual_obj_ind = len(ms_oracle.levels[level].oracle.data) - 1
    if len(concat_obj) > 0 and\
            csc.compute_signal_similarity(ms_oracle, level, actual_obj_ind - 1, actual_obj_ind) > prm.teta:
        return 0
    return 1

def rule_3b_repetition_paradigm_seg(ms_oracle, level):
    concat_obj = ms_oracle.levels[level].concat_obj.extConcatNote.concatNote.concat_labels
    actual_obj_ind = len(ms_oracle.levels[level].oracle.data) - 1
    if len(concat_obj) > 1 and \
            csc.compute_signal_similarity(ms_oracle, level, actual_obj_ind - 2, actual_obj_ind -1) > prm.teta and \
            csc.compute_signal_similarity(ms_oracle, level, actual_obj_ind - 1, actual_obj_ind) < prm.teta:
        return 1
    return 0

sigRule_tab = [[rule1_dissimilarity, 0, rule_3a_repetition_paradigm_noseg],
                [0, rule2_isolated_object, rule_3b_repetition_paradigm_seg]]

