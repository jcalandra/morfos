import numpy as np
from Bio import pairwise2
from Bio.Align import substitution_matrices
import parameters

# In this file are computed the alignment between strings to compute similarity at a symbolic scale

transpo = parameters.TRANSPOSITION
quotient = parameters.QUOTIENT
threshold = parameters.TETA

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
    np_mat = np.array(mat[1])*quotient
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
    if similarity >= threshold*quotient:
        print(nw_align[0][0], nw_align[0][1])
        print("tabTransfo", tabTransfo(nw_align[0][0], nw_align[0][1], [], gap))
        return 1, similarity
    return 0, similarity


# ================================== MATERIALS TRANSFORMATION FUNCTIONS ================================================
def tabTransfo(mat_rep, mat_obj, transfo_tabs, gap=gap):
    i = 0
    id_mk = 1
    id_ext = id_red = 0
    len_gap = 0
    str_gap = ''
    shift = 0
    while i < len(mat_rep):
        if mat_obj[i] == gap:
            if id_ext == 1:
                transfo_tabs.append(['extension', i-len(str_gap) - shift, str_gap])
                id_ext = 0
                str_gap = ''
            len_gap += 1
            id_mk = 0
            id_red = 1
        elif mat_rep[i] == gap:
            if id_red == 1:
                transfo_tabs.append(['reduction', i-len_gap - shift, len_gap])
                shift += len_gap
                id_red = 0
                len_gap = 0
            str_gap += mat_obj[i]
            id_mk = 0
            id_ext = 1
        else:
            if id_red == 1:
                transfo_tabs.append(['reduction', i-len_gap - shift, len_gap])
                shift += len_gap
                id_red = 0
                len_gap = 0
            if id_ext == 1:
                transfo_tabs.append(['extension', i-len(str_gap) - shift, str_gap])
                id_ext = 0
                str_gap = ''
            if mat_rep[i] != mat_obj[i]:
                transfo_tabs.append(['variation', i - shift, mat_obj[i]])
                id_mk = 0
        i += 1
    if id_red == 1:
        transfo_tabs.append(['reduction', i - len_gap - shift, len_gap])
    elif id_ext == 1:
        transfo_tabs.append(['extension', i - len(str_gap) - shift, str_gap])
    elif id_mk == 1:
        transfo_tabs.append(['identity'])
    return transfo_tabs


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


def get_mat_obj(mat_rep, transfo_tabs):
    mat_obj = mat_rep
    for i in transfo_tabs:
        if i[0] == 'identity':
            mat_obj = identity(mat_obj)
        if i[0] == 'variation':
            mat_obj = variation(mat_obj, i[1], i[2])
        if i[0] == 'extension':
            mat_obj = extension(mat_obj, i[1], i[2])
        if i[0] == 'reduction':
            mat_obj = reduction(mat_obj, i[1], i[2])
    return mat_obj

# ================================= STRUCTURE TRANSFORMATION FUNCTIONS =================================================
