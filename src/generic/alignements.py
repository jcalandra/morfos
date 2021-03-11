import numpy as np
from Bio import pairwise2
from Bio.Align import substitution_matrices
import parameters

TRANSPOSITION = 0
quotient = parameters.QUOTIENT
threshold = parameters.TETA


def scheme_alignement(string_compared, actual_string, mat):
    # initalisation
    alignment = -pow(10, 10)
    if len(actual_string) == 0:
        return 0, 0
    min_len = min(len(string_compared), len(actual_string))
    '''min_char = ord(min(min(string_compared), min(actual_string)))
    max_char = ord(max(max(string_compared), max(actual_string)))'''
    if TRANSPOSITION:
        transpo = 1  # max_char - min_char
    else:
        transpo = 1

    # NW parameters
    gap_value = -10
    extend_gap_value = -5
    gap = chr(0)

    # creation of the similarity matrix
    if not mat[1]:
        mat[1] = np.empty((0, 0))
    np_mat = np.array(mat[1])*quotient
    matrix = substitution_matrices.Array(alphabet=mat[0], dims=2, data=np_mat)

    # conversion of the string if necessary
    sx = string_compared
    for j in range(transpo):
        sy = ''
        for i in actual_string:
            sy += chr(ord(i) - j)

        # Needleman-Wunsch alignement
        nw_align = pairwise2.align.globalds(sx, sy, matrix, gap_value, extend_gap_value, gap_char=gap)
        if len(nw_align) == 0:
            return 0, 0
        nw_alignment = nw_align[0][2]
        if nw_alignment > alignment:
            alignment = nw_alignment

    similarity = alignment / min_len
    if similarity >= threshold*quotient:
        return 1, similarity
    return 0, similarity
