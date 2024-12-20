import numpy as np
from Bio import pairwise2
from Bio.Align import substitution_matrices
import similarity_functions as sim_f
import version1.parameters as prm
import librosa
import needlemanwunsch as nw

# In this file are computed the alignment between strings to compute similarity at a symbolic scale

transpo = prm.TRANSPOSITION
quotient = prm.QUOTIENT
threshold = prm.TETA

letter_diff = prm.LETTER_DIFF


# ================================================= ALIGNMENT ==========================================================
# penalty values
gap_value = prm.GAP_VALUE
extend_gap_value = prm.EXT_GAP_VALUE
gap = prm.GAP
correc_value = prm.CORREC_VALUE


def compute_alignment(string_compared, actual_string, mat):
    # initalisation
    alignment = -pow(10, 10)
    if len(actual_string) == 0:
        return 0, 0
    min_len = min(len(string_compared), len(actual_string))

    # conversion of the string if necessary
    sx = string_compared
    for j in range(transpo):
        sy = ''
        for i in actual_string:
            sy += chr(ord(i) - j)
        autosim_mat = []
        for i in range(len(mat[1])):
            autosim_mat.append([])
            for j in range(len(mat[1][i])):
                autosim_mat[i].append(mat[1][i][j]*quotient)
        new_mat = [mat[0], autosim_mat]
        # Needleman-Wunsch alignment
        nw_align = nw.nw(sx, sy, new_mat, gap_value = gap_value, gap = gap)
        nw_alignment = nw_align[1]
        if nw_alignment > alignment:
            alignment = nw_alignment

    similarity = (alignment - correc_value) / min_len
    if similarity >= threshold * quotient:
        return 1, similarity
    return 0, similarity

# depreciated alignment computing using biopython.pairwise2 library
def compute_alignment_pairwize(string_compared, actual_string, mat):
    # initalisation
    alignment = -pow(10, 10)
    if len(actual_string) == 0:
        return 0, 0
    min_len = min(len(string_compared), len(actual_string))

    # creation of the similarity matrix
    if not mat[1]:
        mat[1] = np.empty((0, 0))
    np_mat = np.array(mat[1]) * quotient
    matrix = substitution_matrices.Array(alphabet=mat[0], dims=2, data=np_mat)

    # conversion of the string if necessary
    sx = string_compared
    for j in range(transpo):
        sy = ''
        for i in actual_string:
            sy += chr(ord(i) - j)
        # Needleman-Wunsch alignment
        nw_align = pairwise2.align.globalds(sx, sy, matrix, gap_value, extend_gap_value, gap_char=gap)
        if len(nw_align) == 0:
            return 0, 0
        nw_alignment = nw_align[0][2]
        if nw_alignment > alignment:
            alignment = nw_alignment

    similarity = (alignment - correc_value) / min_len
    if similarity >= threshold * quotient:
        # print(nw_align[0][0], nw_align[0][1])
        # print("tabTransfo", lambda_tabTransfo(nw_align[0][0], nw_align[0][1], [], gap))
        return 1, similarity
    return 0, similarity


# ==================================================== SIGNAL ==========================================================
MFCC_BIT = prm.MFCC_BIT
FFT_BIT = prm.FFT_BIT
CQT_BIT = prm.CQT_BIT

rate = prm.SR
nb_value = prm.NB_VALUES

nb_notes = prm.NB_NOTES
NPO = prm.NOTES_PER_OCTAVE
fmin = prm.NOTE_MIN


def compute_window_audio(oracles, level, actual_object):
    # descriptor corresponds to the descriptor that is computed from the actual_object
    descriptor = []
    # TODO: when object structure will be modified,
    #  k_init = actual_object.init,
    #  k_end = k_init + len(actual_object.label) - 1
    k_init = len(oracles[1][level][1]) + 1
    k_end = k_init + len(actual_object) - 1
    if level > 0:
        lv = level - 1
        while lv >= 0:
            link = oracles[1][lv][1]
            link_r = link.copy()
            link_r.reverse()
            k_init = link.index(k_init)
            k_end = len(link) - link_r.index(k_end) - 1

    window = oracles[2][k_init:k_end + 1]
    return window


def compute_descriptor(window):
    hop_length = len(window)
    #if MFCC_BIT:
    descriptor = librosa.feature.mfcc(y=window, sr=rate, hop_length=hop_length, n_mfcc=20)[1:]
    '''elif FFT_BIT:
        descriptor = data_computing.get_frequency_windows(window, rate, 0, hop_length)
    else:
        descriptor = np.abs(librosa.cqt(window, sr=rate, hop_length=hop_length, fmin=librosa.note_to_hz(fmin),
                     n_bins=nb_notes, bins_per_octave=NPO, window='blackmanharris', sparsity=0.01, norm=1))
        descriptor = librosa.amplitude_to_db(descriptor, ref=np.max)'''
    return descriptor


def compute_signal_similarity(s_tab, compared_object_ind):
    # freq_static_sim_fft is ok because s_tab is in the according shape
    similarity = sim_f.frequency_static_similarity(s_tab, compared_object_ind, len(s_tab) - 1)
    if similarity >= threshold:
        return 1, similarity
    return 0, similarity
