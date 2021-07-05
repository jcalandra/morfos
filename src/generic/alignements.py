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
def scheme_alignment(string_compared, actual_string, mat):
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
        print(nw_align[0][0], nw_align[0][1])
        # print("tabTransfo", lambda_tabTransfo(nw_align[0][0], nw_align[0][1], [], gap))
        return 1, similarity
    return 0, similarity


# ================================== MATERIALS TRANSFORMATION FUNCTIONS ================================================

def identity(mat_rep):
    return mat_rep


def variation(mat_rep, ind_mismatch, value_mismatch):
    mat_obj = mat_rep[:ind_mismatch] + value_mismatch
    if len(mat_rep) > ind_mismatch:
        mat_obj += mat_rep[ind_mismatch + 1:]
    return mat_obj


def reduction(mat_rep, ind_gap, len_gap):
    mat_obj = mat_rep[:ind_gap]
    if len(mat_rep) > ind_gap + len_gap:
        mat_obj += mat_rep[ind_gap + len_gap:]
    return mat_obj


def extension(mat_rep, ind_gap, str_gap):
    mat_obj = mat_rep[:ind_gap] + str_gap
    if len(mat_rep) > ind_gap:
        mat_obj += mat_rep[ind_gap:]
    return mat_obj


def lambda_identity():
    return lambda x: identity(x)


def lambda_variation(ind_mismatch, value_mismatch):
    return lambda x: variation(x, ind_mismatch, value_mismatch)


def lambda_reduction(ind_gap, len_gap):
    return lambda x: reduction(x, ind_gap, len_gap)


def lambda_extension(ind_gap, str_gap):
    return lambda x: extension(x, ind_gap, str_gap)


def lambda_tabTransfo(mat_rep, mat_obj, transfo_tabs, sim_matrix, gap=gap):
    i = 0
    id_mk = 1
    id_ext = id_red = 0
    len_gap = 0
    str_gap = ''
    shift = 0
    len_mat = len(mat_rep)
    while i < len_mat:
        if mat_obj[i] == gap:
            if id_ext == 1:
                transfo_tabs.append([lambda_extension(i - len(str_gap) - shift, str_gap),
                                     'extension', (i - len(str_gap) - shift, str_gap),
                                     gap_value + (len(str_gap) - 1)*extend_gap_value])
                id_ext = 0
                str_gap = ''
            len_gap += 1
            id_mk = 0
            id_red = 1
        elif mat_rep[i] == gap:
            if id_red == 1:
                transfo_tabs.append([lambda_reduction(i - len_gap - shift, len_gap),
                                     'reduction', (i - len_gap - shift, len_gap),
                                     gap_value + (len_gap - 1)*extend_gap_value])
                shift += len_gap
                id_red = 0
                len_gap = 0
            str_gap += mat_obj[i]
            id_mk = 0
            id_ext = 1
        else:
            if id_red == 1:
                transfo_tabs.append([lambda_reduction(i - len_gap - shift, len_gap),
                                     'reduction', (i - len_gap - shift, len_gap),
                                     gap_value + (len_gap - 1)*extend_gap_value])
                shift += len_gap
                id_red = 0
                len_gap = 0
            if id_ext == 1:
                transfo_tabs.append([lambda_extension(i - len(str_gap) - shift, str_gap),
                                     'extension', (i - len(str_gap) - shift, str_gap),
                                     gap_value + (len(str_gap) - 1)*extend_gap_value])
                id_ext = 0
                str_gap = ''
            if mat_rep[i] != mat_obj[i]:
                transfo_tabs.append([lambda_variation(i - shift, mat_obj[i]), 'variation', (i - shift, mat_obj[i]),
                                     1 - sim_matrix[1][ord(mat_rep[i]) - letter_diff]
                                     [(ord(mat_obj[i]) - letter_diff)]])
                id_mk = 0
        i += 1
    if id_red == 1:
        transfo_tabs.append([lambda_reduction(i - len_gap - shift, len_gap),
                             'reduction', (i - len_gap - shift, len_gap),
                             gap_value + (len_gap - 1)*extend_gap_value])
    elif id_ext == 1:
        transfo_tabs.append([lambda_extension(i - len(str_gap) - shift, str_gap),
                             'extension', (i - len(str_gap) - shift, str_gap),
                             gap_value + (len(str_gap) - 1)*extend_gap_value])
    elif id_mk == 1:
        transfo_tabs.append([lambda_identity(), 'identity', (), 0])
    return transfo_tabs


def lambda_get_mat_obj(mat_rep, transfo_tabs):
    mat_obj = mat_rep
    for fun, fun_label, params, weight in transfo_tabs:
        mat_obj = fun(mat_obj)
    return mat_obj


def transfo_similarity(transfo_tabs_ref, transfo_tabs_obj, min_len):
    diff = 1
    for i in range(len(transfo_tabs_ref)):
        diff -= transfo_tabs_ref[i][3]/min_len
        for j in range(len(transfo_tabs_obj)):
            if transfo_tabs_ref[i] == transfo_tabs_obj[j]:
                diff += 2*transfo_tabs_ref[i][3]/min_len
    for j in range(len(transfo_tabs_obj)):
        diff -= transfo_tabs_obj[j][3]/min_len
    return 1 - diff

# ================================= STRUCTURE TRANSFORMATION FUNCTIONS =================================================
