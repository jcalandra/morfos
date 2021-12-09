import numpy as np
from Bio import pairwise2
from Bio.Align import substitution_matrices
import similarity_functions as sim_f
import parameters
import librosa
import data_computing

# In this file are computed the alignment between strings to compute similarity at a symbolic scale

transpo = parameters.TRANSPOSITION
quotient = parameters.QUOTIENT
threshold = parameters.TETA

letter_diff = parameters.LETTER_DIFF


# ================================================= ALIGNMENT ==========================================================
# penalty values
gap_value = parameters.GAP_VALUE
extend_gap_value = parameters.EXT_GAP_VALUE
gap = parameters.GAP
correc_value = parameters.CORREC_VALUE


def compute_alignment(string_compared, actual_string, mat, level=0):
    # initalisation
    alignment = -pow(10, 10)
    if len(actual_string) == 0:
        return 0, 0
    min_len = min(len(string_compared), len(actual_string))

    # creation of the similarity matrix
    if not mat.values:
        mat.values = np.empty((0, 0))
    np_mat = np.array(mat.values) * quotient
    matrix = substitution_matrices.Array(alphabet=mat.labels, dims=2, data=np_mat)
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
MFCC_BIT = parameters.MFCC_BIT
FFT_BIT = parameters.FFT_BIT
CQT_BIT = parameters.CQT_BIT

rate = parameters.SR
nb_value = parameters.NB_VALUES

nb_notes = parameters.NB_NOTES
NPO = parameters.NOTES_PER_OCTAVE
fmin = parameters.NOTE_MIN


def compute_signal_similarity(concat_tab, mean_tab, compared_object_ind):
    # freq_static_sim_fft is ok because s_tab is in the according shape
    '''similarity = 0
    for i in range(len(concat_tab)):
        print("oh", len(concat_tab[i][compared_object_ind]), concat_tab[i][compared_object_ind])
        print("ah", len(concat_tab[i][len(concat_tab[i]) - 1]), concat_tab[i][len(concat_tab[i]) - 1])
        similarity += sim_f.frequency_static_similarity_cqt(concat_tab[i], compared_object_ind, len(concat_tab[i]) - 1)
    similarity = similarity/len(concat_tab)
    if similarity >= threshold:
        return 1, similarity'''
    similarity = sim_f.frequency_static_similarity(mean_tab, compared_object_ind, len(mean_tab) - 1)
    if similarity >= 0.944:
        print("material", len(mean_tab))
        return 1, similarity
    return 0, similarity
