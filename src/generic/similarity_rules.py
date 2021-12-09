import similarity_computation
from parameters import LETTER_DIFF, STRICT_EQUALITY, ALIGNMENT
letter_diff = LETTER_DIFF


# ================================================ SIMILARITY ==========================================================
def similarity_strict(oracles, level):
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    sim_tab = [0 for ind in range(len(history_next))]
    for i in range(len(history_next)):
        if len(concat_obj) == len(history_next[i][1]):
            j = 0
            while history_next[i][1][j] == concat_obj[j]:
                j = j + 1
                if j == len(history_next[i][1]):
                    new_char = history_next[i][0]
                    return new_char, None, sim_tab, 1
    return None, None, sim_tab, 0


def similarity_alignment(oracles, level):
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    if level > 0:
        matrix = oracles[1][level - 1][6]
    else:
        matrix = oracles[1][level][7]
    sim_tab = []
    for i in range(len(history_next)):
        sim_digit, sim_value = similarity_computation.compute_alignment(history_next[i][1], concat_obj, matrix)
        sim_tab.append(sim_value / similarity_computation.quotient)
        if sim_digit:
            new_char = history_next[i][0]
            return new_char, None, sim_tab, 1
    return None, None, sim_tab, 0


def similarity_signal(oracles, level):
    sim_tab = []
    s_tab = []
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    window = similarity_computation.compute_window_audio(oracles, level, concat_obj)
    actual_object_descriptor = similarity_computation.compute_descriptor(window)
    s_tab.append(actual_object_descriptor)
    for i in range(len(history_next)):
        # s_tab corresponds to the descriptors from history_next_table concatenated with the descriptor extracted
        # from actual_obj
        s_tab.append(history_next[i][2])
        sim_digit, sim_value = similarity_computation.compute_signal_similarity(s_tab, i)
        sim_tab.append(sim_value)
        if sim_digit:
            new_char = history_next[i][0]
            return new_char, actual_object_descriptor, sim_tab, 1
    s_tab.pop(0)
    return None, None, sim_tab, 0


def char_next_level_similarity(oracles, level):
    """ The function compare the actual new structured string with structured strings already seen before. For now,
    the strings have to be the exact sames to be considered as similar. The history_next tab is modified according to
    the results and the new string of upper level new_char is returned."""
    # put here the similarity function that interest you
    # similarity_strict
    # similarity_alignment
    # similarity_signal
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    matrix_next = oracles[1][level][6]

    if level == 0:
        matrix = oracles[1][level][7]
    else:
        matrix = oracles[1][level - 1][6]
    if STRICT_EQUALITY:
        new_char, new_descriptor, sim_tab, digit = similarity_strict(oracles, level)
    elif ALIGNMENT:
        new_char, new_descriptor, sim_tab, digit = similarity_alignment(oracles, level)
    else:
        new_char, new_descriptor, sim_tab, digit = similarity_alignment(oracles, level)
    if digit:
        return new_char

    new_char = chr(letter_diff + len(history_next) + 1)
    sim_tab.append(1)
    matrix_next[0] += new_char
    matrix_next[1].append(sim_tab.copy())
    for i in range(len(matrix_next[1]) - 1):
        matrix_next[1][i].append(matrix_next[1][len(matrix_next[1]) - 1][i])

    history_next.append((new_char, concat_obj, new_descriptor))
    return new_char


