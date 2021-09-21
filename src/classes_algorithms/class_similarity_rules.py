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


def similarity(ms_oracle, level):
    if level > 0:
        matrix = ms_oracle.levels[level - 1].materials.sim_matrix
    else:
        matrix = ms_oracle.matrix

    sim_tab_label = s_tab_concat = []

    window = ms_oracle.levels[level].concat_obj.concat_signal
    actual_object_descriptor = class_object.Descriptors()
    actual_object_descriptor.compute(window)
    for i in range(actual_object_descriptor.nb_descriptors):
        s_tab_concat = [[actual_object_descriptor.concat_descriptors[i]]]
    s_tab_mean = [actual_object_descriptor.mean_descriptors]

    for i in range(len(ms_oracle.levels[level].materials.history)):
        # compute alignment from labels
        sim_digit_label, sim_value = class_similarity_computation.compute_alignment(
            ms_oracle.levels[level].materials.history[i][1], ms_oracle.levels[level].concat_obj.concat_labels, matrix,
            level)
        sim_tab_label.append(sim_value / class_similarity_computation.quotient)

        # compute similarity from signal
        for j in range(actual_object_descriptor.nb_descriptors):
            s_tab_concat[j].append(ms_oracle.levels[level].materials.history[i][0].descriptors.concat_descriptors[j])
        s_tab_mean.append(ms_oracle.levels[level].materials.history[i][0].descriptors.mean_descriptors)
        sim_digit_descriptors = class_similarity_computation.compute_signal_similarity(s_tab_concat, s_tab_mean, i)

        if sim_digit_label and sim_digit_descriptors:
            new_rep = ms_oracle.levels[level].materials.history[i][0]
            new_rep. update(window, new_rep.label, actual_object_descriptor)
            return new_rep, sim_tab_label

    # compute new representative
    new_char = chr(letter_diff + len(ms_oracle.levels[level].materials.history) + 1)
    new_rep = class_object.ObjRep()
    new_rep.init(ms_oracle.levels[level].concat_obj.concat_signal, new_char, actual_object_descriptor)
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


