import class_similarity_computation
from parameters import LETTER_DIFF
letter_diff = LETTER_DIFF


# ================================================ SIMILARITY ==========================================================
def similarity_strict(ms_oracle, level):
    history_next = ms_oracle.levels[level].materials.history
    concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
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


def similarity_alignment(ms_oracle, level):
    if level > 0:
        matrix = ms_oracle.levels[level - 1].materials.sim_matrix
    else:
        matrix = ms_oracle.matrix
    sim_tab = []
    for i in range(len(ms_oracle.levels[level].materials.history)):
        sim_digit, sim_value = class_similarity_computation.compute_alignment(
            ms_oracle.levels[level].materials.history[i][1], ms_oracle.levels[level].concat_obj.concat_labels, matrix)
        sim_tab.append(sim_value / class_similarity_computation.quotient)
        if sim_digit:
            new_char = ms_oracle.levels[level].materials.history[i][0]
            return new_char, None, sim_tab, 1
    return None, None, sim_tab, 0


def similarity_signal(ms_oracle, level):
    sim_tab = []
    s_tab = []
    history_next = ms_oracle.levels[level].materials.history
    concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
    window = class_similarity_computation.compute_window_audio(ms_oracle, level, concat_obj)
    actual_object_descriptor = class_similarity_computation.compute_descriptor(window)
    s_tab.append(actual_object_descriptor)
    for i in range(len(history_next)):
        # s_tab corresponds to the descriptors from history_next_table concatenated with the descriptor extracted
        # from actual_obj
        s_tab.append(history_next[i][2])
        sim_digit, sim_value = class_similarity_computation.compute_signal_similarity(s_tab, i)
        sim_tab.append(sim_value)
        if sim_digit:
            new_char = history_next[i][0]
            return new_char, actual_object_descriptor, sim_tab, 1
    s_tab.pop(0)
    return None, None, sim_tab, 0


def char_next_level_similarity(ms_oracle, level):
    """ The function compare the actual new structured string with structured strings already seen before. For now,
    the strings have to be the exact sames to be considered as similar. The history_next tab is modified according to
    the results and the new string of upper level new_char is returned."""
    # put here the similarity function that interest you
    # similarity_strict
    # similarity_alignment
    # similarity_signal

    new_char, new_descriptor, sim_tab, digit = similarity_alignment(ms_oracle, level)
    if digit:
        return new_char

    new_char = chr(letter_diff + len(ms_oracle.levels[level].materials.history) + 1)
    sim_tab.append(1)
    ms_oracle.levels[level].materials.sim_matrix.labels += new_char
    ms_oracle.levels[level].materials.sim_matrix.values.append(sim_tab.copy())
    for i in range(len(ms_oracle.levels[level].materials.sim_matrix.values) - 1):
        ms_oracle.levels[level].materials.sim_matrix.values[i].append(
            ms_oracle.levels[level].materials.sim_matrix.values[len(
                ms_oracle.levels[level].materials.sim_matrix.values) - 1][i])

    ms_oracle.levels[level].materials.history.append((new_char, ms_oracle.levels[level].concat_obj.concat_labels))
    return new_char


