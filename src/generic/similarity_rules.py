import alignments
from parameters import LETTER_DIFF
letter_diff = LETTER_DIFF


# ================================================ SIMILARITY ==========================================================
def similarity_strict(history_next, concat_obj, matrix):
    sim_tab = [0 for ind in range(len(history_next))]
    for i in range(len(history_next)):
        if len(concat_obj) == len(history_next[i][1]):
            j = 0
            while history_next[i][1][j] == concat_obj[j]:
                j = j + 1
                if j == len(history_next[i][1]):
                    new_char = history_next[i][0]
                    return new_char, sim_tab, 1
    return None, sim_tab, 0


def similarity_alignment(history_next, concat_obj, matrix):
    sim_tab = []
    for i in range(len(history_next)):
        sim_digit, sim_value = alignments.compute_alignment(history_next[i][1], concat_obj, matrix)
        sim_tab.append(sim_value / alignments.quotient)
        if sim_digit:
            new_char = history_next[i][0]
            return new_char, sim_tab, 1
    return None, sim_tab, 0


def similarity_signal(history_next, concat_obj, matrix):
    sim_tab = []
    sim_digit = 0
    for i in range(len(history_next)):
        # TODO: implémenter la similarité à partir du signal à tous les niveaux
        if sim_digit:
            new_char = history_next[i][0]
            return new_char, sim_tab, 1
    return None, sim_tab, 0


def char_next_level_similarity(history_next, matrix, matrix_next, concat_obj):
    """ The function compare the actual new structured string with structured strings already seen before. For now,
    the strings have to be the exact sames to be considered as similar. The history_next tab is modified according to
    the results and the new string of upper level new_char is returned."""
    # put here the similarity function that interest you
    # similarity_strict
    # similarity_alignment
    # similarity_signal
    new_char, sim_tab, digit = similarity_alignment(history_next, concat_obj, matrix)
    if digit:
        return new_char

    new_char = chr(letter_diff + len(history_next) + 1)
    sim_tab.append(1)
    matrix_next[0] += new_char
    matrix_next[1].append(sim_tab.copy())
    for i in range(len(matrix_next[1]) - 1):
        matrix_next[1][i].append(matrix_next[1][len(matrix_next[1]) - 1][i])

    history_next.append((new_char, concat_obj))
    return new_char


