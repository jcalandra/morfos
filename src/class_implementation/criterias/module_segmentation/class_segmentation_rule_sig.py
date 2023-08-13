import parameters as prm

RULE_1 = DIFF_FOURIER
RULE_2 = DIFF_DYNAMIC


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
        return 1
    return 0

sigRule_tab = [[rule_1_similarity_word, rule_2_existing_object, rule_3_recomputed_object, 0, 0, rule_6b_high_bound, rule_7b_mean_word_length_high, rule_8b_repetition_paradigm_seg],
                [0, 0, 0, rule_4_not_validated_hypothesis, rule_5_regathering_after, rule_6a_low_bound, rule_7a_mean_word_length_low, rule_8a_repetition_paradigm_noseg]]

