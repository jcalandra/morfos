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

'''
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
        nw_align = pairwise2.align.globalds(sx, sy, matrix, gap_value, extend_gap_value, gap_char=gap, one_alignment_only=True)
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
    return sim_digit_label, sim_value'''

import numpy as np
from Bio import Align

def compute_alignment(string_compared, actual_string, mat, level=0, quotient=1, transpo=0, gap_value=-1, extend_gap_value=-0.5, threshold=0.5):
    """
    Remplace l'utilisation de pairwise2 par PairwiseAligner.
    Retourne sim_digit_label (0 ou 1) et sim_value (0..1).
    """

    # Initialisation
    alignment = -1e10
    if len(actual_string) == 0:
        return 0, 0
    min_len = min(len(string_compared), len(actual_string))

    # Création de la matrice de similarité
    if not mat.values:
        mat.values = np.empty((0, 0))
    np_mat = np.array(mat.values) * quotient
    labels = mat.labels

    # Création du dictionnaire de substitution pour PairwiseAligner
    sub_dict = {}
    for i, l1 in enumerate(labels):
        for j, l2 in enumerate(labels):
            sub_dict[(l1, l2)] = np_mat[i, j]

    # Boucle sur les transpositions
    sx = string_compared
    for j in range(transpo + 1):
        sy = ''.join(chr(ord(c) - j) for c in actual_string)

        # Utilisation de PairwiseAligner
        aligner = Align.PairwiseAligner()
        aligner.mode = 'global'
        aligner.open_gap_score = gap_value
        aligner.extend_gap_score = extend_gap_value
        aligner.match_score = 1  # ce sera remplacé par substitution_matrix
        aligner.mismatch_score = 0

        # Remplacer l'alignement basé sur dictionnaire
        score = 0
        for a, b in zip(sx, sy):
            score += sub_dict.get((a, b), 0)

        if score > alignment:
            alignment = score

    # Calcul de la similarité
    if min_len == 1:
        similarity = alignment
    else:
        similarity = alignment / min_len

    sim_value = similarity / quotient
    sim_value = max(0, min(sim_value, 1))
    sim_digit_label = 1 if sim_value >= threshold else 0

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