import class_similarity_rules_symb
import class_similarity_rules_sig as sim_f
from object_model import class_object
import class_concatObj
from module_parameters.parameters import LETTER_DIFF, processing, teta, STRICT_EQUALITY, ALIGNMENT
letter_diff = LETTER_DIFF

def compute_signal_similarity_old(concat_tab, mean_tab, compared_object_ind):
    # freq_static_sim_fft is ok because s_tab is in the according shape
    '''similarity = 0
    for i in range(len(concat_tab)):
        similarity += sim_f.frequency_static_similarity_cqt(concat_tab[i], compared_object_ind, len(concat_tab[i]) - 1)
    similarity = similarity/len(concat_tab)
    if similarity >= threshold:
        return 1, similarity'''
    similarity = sim_f.frequency_static_similarity(mean_tab, compared_object_ind, len(mean_tab) - 1)
    if similarity >= teta:
        return 1, similarity
    return 0, similarity

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
        sim_digit, sim_value = class_similarity_rules_symb.compute_alignment(
            ms_oracle.levels[level].materials.history[i][1], ms_oracle.levels[level].concat_obj.concat_labels, matrix, level)
        sim_tab.append(sim_value / class_similarity_rules_symb.quotient)
        if sim_digit:
            new_char = ms_oracle.levels[level].materials.history[i][0]
            return new_char, None, sim_tab, 1
    return None, None, sim_tab, 0


def similarity_old(ms_oracle, level):
    if level > 0:
        matrix = ms_oracle.levels[level - 1].materials.sim_matrix
    else:
        matrix = ms_oracle.matrix
    sim_tab_label = []

    window = ms_oracle.levels[level].concat_obj.concat_signal
    actual_object_descriptor = class_object.Descriptors()
    actual_object_descriptor.copy(ms_oracle.levels[level].concat_obj.descriptors)
    s_tab_concat = actual_object_descriptor.concat_descriptors
    s_tab_mean = actual_object_descriptor.mean_descriptors

    for i in range(len(ms_oracle.levels[level].materials.history)):
        # compute similarity from labels
        if STRICT_EQUALITY:

            concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
            history_next_i = ms_oracle.levels[level].materials.history[i][1].concat_labels

            sim_digit_label = 0
            if len(concat_obj) == len(history_next_i):
                j = 0
                while history_next_i[j] == concat_obj[j]:
                    j = j + 1
                    if j == len(history_next_i):
                        sim_digit_label = 1
                        break
            sim_value = sim_digit_label * class_similarity_rules_symb.quotient
        elif ALIGNMENT:
            sim_digit_label, sim_value = class_similarity_rules_symb.compute_alignment(
                ms_oracle.levels[level].materials.history[i][1].concat_labels,
                ms_oracle.levels[level].concat_obj.concat_labels, matrix, level)
        else:
            sim_digit_label, sim_value = class_similarity_rules_symb.compute_alignment(
                ms_oracle.levels[level].materials.history[i][1].concat_labels,
                ms_oracle.levels[level].concat_obj.concat_labels, matrix, level)
        sim_tab_label.append(sim_value / class_similarity_rules_symb.quotient)

        # compute similarity from signal
        if processing != "symbols":
            for j in range(actual_object_descriptor.nb_descriptors):
                s_tab_concat.append(ms_oracle.levels[level].materials.history[i][0].descriptors.concat_descriptors[j])
                s_tab_mean.append(ms_oracle.levels[level].materials.history[i][0].descriptors.mean_descriptors[j])
            sim_digit_descriptors, sim_tab_descriptor = class_similarity_rules_symb.compute_signal_similarity(
                s_tab_concat, s_tab_mean, 0)

            if sim_digit_descriptors and level == 0 and i == 0:
                sim_digit_descriptors = 0

            if sim_digit_descriptors:
                new_rep = ms_oracle.levels[level].materials.history[i][0]
                # TODO: jcalandra 22/09/2021 maj le reorésentant (corriger le code, bug)
                new_rep.update(window, new_rep.label, actual_object_descriptor)
                return new_rep, sim_tab_label, 1
        if processing == "symbols" and sim_digit_label:
            new_rep = ms_oracle.levels[level].materials.history[i][0]
            return new_rep, sim_tab_label, 1


    # compute new representative
    new_char = chr(letter_diff + len(ms_oracle.levels[level].materials.history) + 1)
    new_rep = class_object.ObjRep()
    new_rep.init(ms_oracle.levels[level].concat_obj.concat_signal, new_char, actual_object_descriptor)
    return new_rep, sim_tab_label, 0

def char_next_level_similarity_old(ms_oracle, level):
    """ The function compare the actual new structured string with structured strings already seen before. For now,
    the strings have to be the exact sames to be considered as similar. The history_next tab is modified according to
    the results and the new string of upper level new_char is returned."""
    new_rep, sim_tab, sim_digit = similarity_old(ms_oracle, level)

    # new_obj update
    new_signal = ms_oracle.levels[level].concat_obj.concat_signal
    new_descriptors = ms_oracle.levels[level].concat_obj.descriptors

    new_obj = class_object.Object()
    new_obj.update(new_rep.label, new_descriptors, new_signal, new_rep)

    if sim_digit:
        return [new_obj]

    # material.sim_matrix update
    sim_tab.append(1)
    ms_oracle.levels[level].materials.sim_matrix.labels += new_rep.label
    ms_oracle.levels[level].materials.sim_matrix.values.append(sim_tab.copy())
    for i in range(len(ms_oracle.levels[level].materials.sim_matrix.values) - 1):
        ms_oracle.levels[level].materials.sim_matrix.values[i].append(
            ms_oracle.levels[level].materials.sim_matrix.values[len(
                ms_oracle.levels[level].materials.sim_matrix.values) - 1][i])

    # material.history update
    #concat_rep = class_concatObj.ConcatObj()
    #concat_rep.init(ms_oracle.levels[level].concat_obj.objects[0].obj_rep)
    #for i in range(1, ms_oracle.levels[level].concat_obj.size):
    #    concat_rep.update(ms_oracle.levels[level].concat_obj.objects[i].obj_rep)
    concat_rep = ms_oracle.levels[level].concat_obj
    ms_oracle.levels[level].materials.history.append((new_rep, concat_rep))
    return [new_obj]
