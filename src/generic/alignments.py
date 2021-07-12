import numpy as np
from Bio import pairwise2
from Bio.Align import substitution_matrices
import parameters

# In this file are computed the alignment between strings to compute similarity at a symbolic scale

transpo = parameters.TRANSPOSITION
quotient = parameters.QUOTIENT
threshold = parameters.TETA

letter_diff = parameters.LETTER_DIFF

# penalty values
gap_value = parameters.GAP_VALUE
extend_gap_value = parameters.EXT_GAP_VALUE
gap = parameters.GAP
correc_value = parameters.CORREC_VALUE


# ================================================= ALIGNMENT ==========================================================
def compute_alignment(string_compared, actual_string, mat):
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


