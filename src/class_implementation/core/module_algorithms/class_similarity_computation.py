import numpy as np
from Bio import pairwise2
from Bio.Align import substitution_matrices
import class_similarity_functions as sim_f
from module_parameters import parameters
import class_materialsMemory

# In this file are computed the alignment between strings to compute similarity at a symbolic scale

transpo = parameters.TRANSPOSITION
quotient = parameters.QUOTIENT
threshold = parameters.TETA
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
    if min_len == 1:
        similarity = nw_alignment
    else:
        similarity = (alignment - correc_value) / min_len
    if similarity >= threshold * quotient:
         return 1, similarity/quotient
    return 0, similarity/quotient


# ==================================================== SIGNAL ==========================================================
MFCC_BIT = parameters.MFCC_BIT
FFT_BIT = parameters.FFT_BIT
CQT_BIT = parameters.CQT_BIT

rate = parameters.SR
nb_value = parameters.NB_VALUES

nb_notes = parameters.NB_NOTES
NPO = parameters.NOTES_PER_OCTAVE
fmin = parameters.NOTE_MIN


def compute_signal_similarity_old(concat_tab, mean_tab, compared_object_ind):
    # freq_static_sim_fft is ok because s_tab is in the according shape
    '''similarity = 0
    for i in range(len(concat_tab)):
        similarity += sim_f.frequency_static_similarity_cqt(concat_tab[i], compared_object_ind, len(concat_tab[i]) - 1)
    similarity = similarity/len(concat_tab)
    if similarity >= threshold:
        return 1, similarity'''
    similarity = sim_f.frequency_static_similarity(mean_tab, compared_object_ind, len(mean_tab) - 1)
    if similarity >= parameters.teta:
        return 1, similarity
    return 0, similarity

def compute_signal_similarity_sim(ms_oracle, level, obj_compared, actual_obj):
    # freq_static_sim_fft is ok because s_tab is in the according shape
    s_tab_all = ms_oracle.levels[level + 1].compute_stab()
    s_tab = s_tab_all[1][0]
    similarity = sim_f.frequency_static_similarity(s_tab, obj_compared, actual_obj)
    return similarity


def compute_symbol_similarity_sim(ms_oracle, level, obj_compared_ind, actual_obj_ind):
    if level > 0:
        if level-1 > 0:
            matrix = ms_oracle.levels[level - 2].materials.sim_matrix
        else:
            matrix = ms_oracle.matrix
    if level == 0:
        obj_compared = ms_oracle.levels[level].objects[obj_compared_ind].label
        actual_obj = ms_oracle.levels[level].objects[actual_obj_ind].label
        matrix = class_materialsMemory.SimMatrix()
        matrix.labels = ''
        matrix.values = [[0 for i in range(len(ms_oracle.symbol))] for j in range(len(ms_oracle.symbol))]
        for i in range(len(ms_oracle.symbol)):
            matrix.labels += chr(parameters.LETTER_DIFF + i)
            matrix.values[i][i] = 1

    else:
        label = ms_oracle.levels[level].oracle.data[obj_compared_ind + 1]
        obj_compared = ms_oracle.levels[level- 1].materials.history[label][1].concat_labels
        actual_obj = ms_oracle.levels[level - 1].concat_obj.concat_labels
    if parameters.STRICT_EQUALITY:
        #concat_obj = ms_oracle.levels[level].concat_obj.concat_labels

        sim_digit_label = 0
        if len(actual_obj) == len(obj_compared):
            j = 0
            while obj_compared[j] == actual_obj[j]:
                j = j + 1
                if j == len(obj_compared):
                    sim_digit_label = 1
                    break
        sim_value = sim_digit_label
    elif parameters.ALIGNMENT:
        sim_digit_label, sim_value = compute_alignment(
            obj_compared,
            actual_obj, matrix, level)
    else:
        sim_digit_label, sim_value = compute_alignment(
            obj_compared,
            actual_obj, matrix, level)
    return sim_value