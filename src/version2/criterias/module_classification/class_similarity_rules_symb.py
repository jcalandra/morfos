import numpy as np
from Bio import pairwise2
from Bio.Align import substitution_matrices

from module_parameters import parameters

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
        #similarity = (alignment - correc_value) / min_len
        similarity = (alignment) / min_len
    sim_value = similarity/quotient
    if sim_value < 0:
        sim_value = 0
    if sim_value > 1:
        sim_value = 1
    if sim_value >= threshold:
        sim_digit_label = 1
    else:
        sim_digit_label = 0
    return sim_digit_label, sim_value


def compute_strict_equality(string_compared, actual_string, mat, level=0):
    sim_digit_label = 0
    if len(actual_string) == len(string_compared):
        j = 0
        while string_compared[j] == actual_string[j]:
            j = j + 1
            if j == len(string_compared):
                sim_digit_label = 1
                break
    sim_value = sim_digit_label
    return sim_digit_label, sim_value