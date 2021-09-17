import class_similarity_computation
import class_object
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
            ms_oracle.levels[level].materials.history[i][1], ms_oracle.levels[level].concat_obj.concat_labels, matrix, level)
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
    for i in range(len(ms_oracle.levels[level].materials.history)):
        # s_tab corresponds to the descriptors from history_next_table concatenated with the descriptor extracted
        # from actual_obj
        s_tab.append(ms_oracle.levels[level].materials.history[i][2])
        sim_digit, sim_value = class_similarity_computation.compute_signal_similarity(s_tab, i)
        sim_tab.append(sim_value)
        if sim_digit:
            new_char = ms_oracle.levels[level].materials.history[i][0]
            return new_char, actual_object_descriptor, sim_tab, 1
    s_tab.pop(0)
    return None, None, sim_tab, 0


def similarity(ms_oracle, level):
    if level > 0:
        matrix = ms_oracle.levels[level - 1].materials.sim_matrix
    else:
        matrix = ms_oracle.matrix

    sim_tab_label = []
    window = class_similarity_computation.compute_window_audio(
        ms_oracle, level, ms_oracle.levels[level].concat_obj.concat_labels)
    actual_object_descriptor = class_similarity_computation.compute_descriptor(window)
    s_tab = [actual_object_descriptor]

    for i in range(len(ms_oracle.levels[level].materials.history)):
        # compute alignment from labels
        sim_digit_label, sim_value = class_similarity_computation.compute_alignment(
            ms_oracle.levels[level].materials.history[i][1], ms_oracle.levels[level].concat_obj.concat_labels, matrix,
            level)
        sim_tab_label.append(sim_value / class_similarity_computation.quotient)

        # compute similarity from signal
        # TODO: jcalandra 17/09/2021 check similarity computation at signal level
        s_tab.append(ms_oracle.levels[level].materials.history[i][2])
        sim_digit_descriptors = class_similarity_computation.compute_signal_similarity(s_tab, i)

        if sim_digit_label and sim_digit_descriptors:
            new_rep = ms_oracle.levels[level].materials.history[i][0]
            # TODO: jcalandra 17/09/2021 update the representative with information of the new object
            return new_rep, sim_tab_label

    # compute new representative
    new_char = chr(letter_diff + len(ms_oracle.levels[level].materials.history) + 1)
    new_rep = class_object.ObjRep()
    new_descriptors = class_object.Descriptors()
    # TODO: jcalandra001 17/09/2021 check new_descriptors.compute function
    new_descriptors.compute(ms_oracle.levels[level].concat_obj.concat_signal)
    new_rep.init(ms_oracle.levels[level].concat_obj.concat_signal, new_char, new_descriptors)
    return new_rep, sim_tab_label


def char_next_level_similarity(ms_oracle, level):
    """ The function compare the actual new structured string with structured strings already seen before. For now,
    the strings have to be the exact sames to be considered as similar. The history_next tab is modified according to
    the results and the new string of upper level new_char is returned."""

    new_rep, sim_tab = similarity(ms_oracle, level)

    # new_obj update
    new_signal = ms_oracle.levels[level].concat_obj.concat_signal
    new_descriptors = class_object.Descriptors()
    new_descriptors.compute(new_signal)

    new_obj = class_object.Object()
    new_obj.update(new_rep.label, new_descriptors, new_signal, new_rep)

    # material.sim_matrix update
    sim_tab.append(1)
    ms_oracle.levels[level].materials.sim_matrix.labels += new_rep.label
    ms_oracle.levels[level].materials.sim_matrix.values.append(sim_tab.copy())
    for i in range(len(ms_oracle.levels[level].materials.sim_matrix.values) - 1):
        ms_oracle.levels[level].materials.sim_matrix.values[i].append(
            ms_oracle.levels[level].materials.sim_matrix.values[len(
                ms_oracle.levels[level].materials.sim_matrix.values) - 1][i])

    # material.history update
    concat_rep = []
    for i in range(ms_oracle.levels[level].concat_obj.size):
        concat_rep.append(ms_oracle.levels[level].concat_obj.objects[i].obj_rep)
    ms_oracle.levels[level].materials.history.append((new_rep, concat_rep))
    return new_obj


