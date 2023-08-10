import class_oracle
import class_similarity_computation
import class_cog_algo
import class_object
import class_concatObj
from module_visualization.formal_diagram_mso import *

# ================================================= RULES ==============================================================
# In this file are implemented the rules that give segmentation criteria
# 5 rules are proposed :
# RULE_1 : Structuring if the actual object has already been seen in the same level of structure.
# RULE_2 : There is no structuring if an hypothesis about the upper level is validated.  RULE_2 is actually the
# opposite of this rule, meaning that there is structuring if no hypothesis is validated.
# RULE_3 : Structuring on this level if the concatenated object is an object already seen on the upper level.
# RULE_4 : RULE_4 is the same rule as RULE_3 except that it takes account of previously unfinished objects that are
# seen again and have then to be modified such as it become an object of upper level.
# RULE_5 : A structured object of upper level which is alone is gathered with the next group.
# On the external parameters, 1 means that the rule is applied and 0 means that the rule is not applied.


# RULE_7 priores to RULE_6 and RULE_6 priores to RULE_5.
# RULE_6 and RULE_7 priores to RULE_8



RULE_1 = prm.RULE_1
RULE_2 = prm.RULE_2
RULE_3 = prm.RULE_3
RULE_4 = prm.RULE_4
RULE_5 = prm.RULE_5
RULE_5b = prm.RULE_5b
RULE_6 = prm.RULE_6
RULE_7 = prm.RULE_7
RULE_8 = prm.RULE_8
ALIGNEMENT_rule3 = prm.ALIGNEMENT_rule3
ALIGNEMENT_rule4 = prm.ALIGNEMENT_rule4

lower_bound_rule6 = prm.lower_bound_rule6
higher_bound_rule6 = prm.higher_bound_rule6

letter_diff = prm.LETTER_DIFF

#====================================
# MANDATORY RULES

# RULE 1:  (ab + a => (ab)(a
#          (ab + b => (abb
def rule_1_similarity_word(ms_oracle, level):
    '''
    if prm.processing == 'signal'and prm.NB_SILENCE > 0 and \
            level == 0 and actual_char == 1:
        return 1'''
    concat_obj_lab = ms_oracle.levels[level].concat_obj.concat_labels
    actual_char = ms_oracle.levels[level].actual_char
    history_next = ms_oracle.levels[level].materials.history
    if len(concat_obj_lab) >= 1 and chr(actual_char + letter_diff) == concat_obj_lab[0]:
        return 1
    for element in history_next:
        if chr(actual_char + letter_diff) == element[1].concat_labels[0]:
            return 1
    return 0


# RULE 2: (ab)(ab + c => (ab)(ab)(c
def rule_2_existing_object(ms_oracle, level):
    """ This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with objects of the upper level stocked in the tab history_next[]. If the strings are similar, returns 1. Otherwise
    the function returns 0."""
    history_next = ms_oracle.levels[level].materials.history
    concat_obj_lab = ms_oracle.levels[level].concat_obj.concat_labels
    actual_char = ms_oracle.levels[level].actual_char
    if level == 0:
        matrix = ms_oracle.matrix
    else:
        matrix = ms_oracle.levels[level - 1].materials.sim_matrix
    if ALIGNEMENT_rule3:
        for i in range(len(history_next)):
            if class_similarity_computation.compute_alignment(history_next[i][1], concat_obj_lab, matrix)[0] and  \
                    class_similarity_computation.compute_alignment(
                        history_next[i][1], concat_obj_lab + chr(actual_char + letter_diff), matrix)[0] == 0:
                return 1
    else:
        for i in range(len(history_next)):
            if history_next[i][1].concat_labels == concat_obj_lab:
                return 1
    return 0



# RULE 4: (abcd)(ab + e => (ab)(cd)(ab)(e
def rule_3_recomputed_object(ms_oracle, level):
    """ This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with substrings of objects of the upper level stocked in the tab history_next[]. If the strings are similar, the
    algorithm goes back to the similar state in the past, structure and recompute the oracles and other structures."""
    # allocation of structures of actual level
    actual_char_ind = ms_oracle.levels[level].actual_char_ind
    f_oracle = ms_oracle.levels[level].oracle
    link = ms_oracle.levels[level].link
    history_next = ms_oracle.levels[level].materials.history
    concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
    k = ms_oracle.levels[level].shift
    nb_elements = len(concat_obj)
    sub_suffix = ""

    if level == 0:
        matrix = ms_oracle.matrix
    else:
        matrix = ms_oracle.levels[level - 1].materials.sim_matrix

    # if there is only one character in concat_obj, that is already seen, it's rule 1
    if nb_elements <= 1:
        return 0

    # if the longest similar suffix is not an adequate value
    if f_oracle.sfx[actual_char_ind - nb_elements] is None or f_oracle.sfx[actual_char_ind - nb_elements] == 0 or\
            f_oracle.sfx[actual_char_ind - nb_elements] == actual_char_ind - nb_elements - 1:
        return 0

    # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
    if ALIGNEMENT_rule4:
        for j in range(nb_elements):
            sub_suffix += chr(f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + j] + letter_diff)
            # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
        if class_similarity_computation.compute_alignment(sub_suffix, concat_obj, matrix)[0] == 0:
            return 0,

    else:
        for j in range(nb_elements):
            if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + j] \
                    != f_oracle.data[actual_char_ind - nb_elements + j]:
                return 0

    # if the the longest similar suffix is constitued of different materials
    for i in range(1, nb_elements):
        if len(link) < f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements + 1 or \
                link[f_oracle.sfx[actual_char_ind - nb_elements] + i - 1] !=\
                link[f_oracle.sfx[actual_char_ind - nb_elements] + i]:
            return 0

    # if the longest similar suffix has only one caracter before it and RULE 5 is activated
    if RULE_5:
        if link[f_oracle.sfx[actual_char_ind - nb_elements]] ==\
                link[f_oracle.sfx[actual_char_ind - nb_elements] - 1] \
                and link[f_oracle.sfx[actual_char_ind - nb_elements] - 1] !=\
                link[f_oracle.sfx[actual_char_ind - nb_elements] - 2]:
            return 0

    # if the actual concat_obj is not the longest common string :
    if ALIGNEMENT_rule4:
        if class_similarity_computation.compute_alignment(
                sub_suffix, concat_obj + chr(f_oracle.data[actual_char_ind] + letter_diff), matrix)[0] == 1:
            return 0
    else:
        if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements] == f_oracle.data[actual_char_ind]:
            return 0

    if len(ms_oracle.levels) > level + 1:

        # allocation of structures of level sup
        f_oracle_sup = ms_oracle.levels[level + 1].oracle
        real_ind = link[f_oracle.sfx[actual_char_ind - nb_elements]]
        real_value = f_oracle_sup.data[real_ind]

        # if concat_obj corresponds to an already known object, return 0.
        if ALIGNEMENT_rule4:
            if class_similarity_computation.compute_alignment(
                    history_next[real_value - 1][1], concat_obj, matrix)[0] == 1 or \
                    class_similarity_computation.compute_alignment(
                    history_next[real_value - 1][1], sub_suffix, matrix)[0] == 1:
                return 0
        else:
            if history_next[real_value - 1][1] == concat_obj:
                return 0

            if link[f_oracle.sfx[actual_char_ind - nb_elements]] != \
                    link[f_oracle.sfx[actual_char_ind - nb_elements] - 1] and \
                    link[f_oracle.sfx[actual_char_ind - nb_elements]] !=\
                    link[f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements]:
                return 0

    # else, we are in the required conditions and we rebuild the oracles
    # we go back to the new already-seen state

    data_length = len(ms_oracle.levels[level].formal_diagram.material_lines[0])
    to_struct = 0
    to_struct_obj = class_concatObj.ConcatObj()

    level_up = level
    level_tmp = -1

    ind = ms_oracle.levels[level].oracle.sfx[actual_char_ind - nb_elements] - 1
    ind_init = ind
    new_ind_p1 = -1
    ind_fo_init = 1
    ind_to_struct = 0

    # each level level_up superior or equal to actual level is recomputed
    while len(ms_oracle.levels) > level_up != level_tmp:
        new_fo = class_oracle.create_oracle('f')

        # f_oracle update
        i = 1
        while i < ind + 1:
            new_state = ms_oracle.levels[level_up].oracle.data[i]
            new_fo.add_state(new_state)
            i += 1

        # compute k_init according to the adequate frame at level 0 for formal diagram representation
        k_init = ind
        frame_level = level_up
        while frame_level > 0:
            k_init = ms_oracle.levels[frame_level - 1].link.index(k_init)
            while len(ms_oracle.levels[frame_level - 1].link) > k_init + 1 \
                    and ms_oracle.levels[frame_level - 1].link[k_init] == \
                    ms_oracle.levels[frame_level - 1].link[k_init + 1]:
                k_init += 1
            frame_level -= 1

        # formal diagram update
        for j in range(len(ms_oracle.levels[level_up].formal_diagram.material_lines)):
            for fd_ind in range(k_init, data_length):
                ms_oracle.levels[level_up].formal_diagram.material_lines[j][fd_ind] = 1
        ms_oracle.levels[level_up].formal_diagram_graph.update(ms_oracle, level_up)

        # link update
        if len(ms_oracle.levels[level_up].link) > ind:
            new_ind = ms_oracle.levels[level_up].link[ind]
            seg = 0
            ms_oracle.levels[level_up].concat_obj.concat_labels = ''
            if len(ms_oracle.levels[level_up].link) > ind + 1:
                new_ind_p1 = ms_oracle.levels[level_up].link[ind + 1]
                if level_up == level and new_ind == new_ind_p1:
                    to_struct = 1
            else:
                new_ind_p1 = ms_oracle.levels[level_up].link[ind]
        else:
            new_ind = max(ms_oracle.levels[level_up].link)
            seg = 1
        while i < len(ms_oracle.levels[level_up].link):
            ms_oracle.levels[level_up].link.pop(i)
        if level_up != level:
            tmp_concat_obj = class_concatObj.ConcatObj()
            if seg == 0 and len(ms_oracle.levels[level_up].link) > 1 and new_ind == new_ind_p1:
                str= ''
                while ms_oracle.levels[level_up].link[len(ms_oracle.levels[level_up].link) - 1] == new_ind:
                    str = chr(ms_oracle.levels[level_up].oracle.data[len(ms_oracle.levels[level_up].link) - 1]
                                         + letter_diff) + str
                    ms_oracle.levels[level_up].link.pop(len(ms_oracle.levels[level_up].link) - 1)

                # concat_obj update
                if len(str) > 0:
                    for el in str:
                        obj = class_object.Object()
                        obj_rep = class_object.ObjRep()
                        obj_rep.update_label(el)
                        obj.update(el, class_object.Descriptors(), [], obj_rep)
                        tmp_concat_obj.update(obj)
                    ms_oracle.levels[level_up].concat_obj.copy(tmp_concat_obj)


            elif seg == 1:
                str = \
                    ms_oracle.levels[level_up].concat_obj.concat_labels[
                    :len(new_fo.data) - len(ms_oracle.levels[level_up].link)]
                if len(str) > 0:
                    concat_obj = class_concatObj.ConcatObj()
                    for el in str:
                        obj = class_object.Object()
                        obj_rep = class_object.ObjRep()
                        obj_rep.update_label(el)
                        obj.update(el, class_object.Descriptors(), [], obj_rep)
                        concat_obj.update(obj)
                    ms_oracle.levels[level_up].concat_obj.copy(concat_obj)

        else:
            if to_struct and len(ms_oracle.levels[level_up].link) > 1:
                # link update and computation of to_struct_obj
                str = ''
                while ms_oracle.levels[level_up].link[len(ms_oracle.levels[level_up].link) - 1] == new_ind:
                    str = chr(ms_oracle.levels[level_up].oracle.data[len(ms_oracle.levels[level_up].link) - 1]
                              + letter_diff) + str
                    ms_oracle.levels[level_up].link.pop(len(ms_oracle.levels[level_up].link) - 1)
                    ind_to_struct += 1
                if len(str) > 0:
                    for el in str:
                        obj = class_object.Object()
                        obj_rep = class_object.ObjRep()
                        obj_rep.update_label(el)
                        obj.update(el, class_object.Descriptors(), [], obj_rep)
                        to_struct_obj.update(obj)

                new_fo = class_oracle.create_oracle('f')
                # f_oracle update
                while ind_fo_init < ind_init + 1 - ind_to_struct:
                    new_state = ms_oracle.levels[level_up].oracle.data[ind_fo_init]
                    new_fo.add_state(new_state)
                    ind_fo_init += 1

                # formal diagram update
                frame_level = level_up
                former_k_init = ind_init
                k_init = ind_init - ind_to_struct
                while frame_level > 0:
                    k_init = ms_oracle.levels[frame_level - 1].link.index(k_init)
                    while len(ms_oracle.levels[frame_level - 1].link) > k_init + 1 and \
                            ms_oracle.levels[frame_level - 1].link[k_init] == \
                            ms_oracle.levels[frame_level - 1].link[k_init + 1]:
                        k_init += 1
                    frame_level -= 1

                for j in range(len(ms_oracle.levels[level_up].formal_diagram.material_lines)):
                    for fd_ind in range(k_init, former_k_init):
                        ms_oracle.levels[level_up].formal_diagram.material_lines[j][fd_ind] = 1
                ms_oracle.levels[level_up].formal_diagram_graph.update(ms_oracle, level_up)

                # history next
                while len(ms_oracle.levels[level_up].materials.history) > max(ms_oracle.levels[level_up].link):
                    ms_oracle.levels[level_up].materials.history.pop()
                    ms_oracle.levels[level_up].materials.sim_matrix.labels = \
                        ms_oracle.levels[level_up].materials.sim_matrix.labels[:-1]
                    ms_oracle.levels[level_up].materials.sim_matrix.values.pop()
                    for mat_line in range(len(ms_oracle.levels[level_up].materials.sim_matrix.values)):
                        ms_oracle.levels[level_up].materials.sim_matrix.values[mat_line].pop()

        new_ind = max(ms_oracle.levels[level_up].link)
        ms_oracle.levels[level_up].oracle = new_fo

        # next level
        level_tmp = level_up
        if level_up < len(ms_oracle.levels) - 1:
            next_ind = max(ms_oracle.levels[level_up + 1].oracle.data[:new_ind + 1])
            len_max = len(ms_oracle.levels[level_up].materials.history)
            for j in range(len_max - next_ind):
                # history_next update
                ms_oracle.levels[level_up].materials.history.pop()
                # matrix update
                ms_oracle.levels[level_up].materials.sim_matrix.labels = \
                    ms_oracle.levels[level_up].materials.sim_matrix.labels[:-1]
                ms_oracle.levels[level_up].materials.sim_matrix.values.pop()
                for mat_line in range(len(ms_oracle.levels[level_up].materials.sim_matrix.values)):
                    ms_oracle.levels[level_up].materials.sim_matrix.values[mat_line].pop()

            ind = new_ind
            level_up = level_up + 1

    # if necessary, compute to_struct_obj and structure
    if to_struct:
        for j in range(ind_to_struct):
            char_ind = ind_fo_init + j
            #TODO: jcalandra 15/09/2021 bugfix
            # débug au niveau signal
            new_state = ms_oracle.levels[level].oracle.data[char_ind]
            ms_oracle.levels[level].actual_char = new_state
            ms_oracle.levels[level].actual_char_ind = char_ind

            ms_oracle.levels[level].oracle.add_state(new_state)

            obj = class_object.Object()
            obj_rep = class_object.ObjRep()
            obj_rep.update_label(to_struct_obj.concat_labels[j])
            obj.update(to_struct_obj.concat_labels[j], class_object.Descriptors(), [], obj_rep)
            ms_oracle.levels[level].concat_obj.update(obj)
            #ms_oracle.levels[level].concat_obj.concat_labels += to_struct_obj[j]
            # formal diagram update at initial level
            ms_oracle.levels[level].formal_diagram.update(ms_oracle, level)
            ms_oracle.levels[level].formal_diagram_graph.update(ms_oracle, level)
        class_cog_algo.structure(ms_oracle, level)
        ms_oracle.levels[level].concat_obj = class_concatObj.ConcatObj()


    # concat_obj update at initial level
    for j in range(nb_elements):
        char_ind = ind_init + j + 1
        new_state = f_oracle.data[char_ind]
        ms_oracle.levels[level].actual_char = new_state
        ms_oracle.levels[level].actual_char_ind = char_ind

        element = chr(new_state + letter_diff)
        obj = class_object.Object()
        obj_rep = class_object.ObjRep()
        obj_rep.update_label(element)
        obj.update(element, class_object.Descriptors(), [], obj_rep)
        ms_oracle.levels[level].concat_obj.update(obj)
        ms_oracle.levels[level].oracle.add_state(new_state)
        # formal diagram update at initial level
        ms_oracle.levels[level].formal_diagram.update(ms_oracle, level)
        ms_oracle.levels[level].formal_diagram_graph.update(ms_oracle, level)
    ms_oracle.levels[level].concat_obj.size = nb_elements

    # Then go back to the main loop of the structuring function with the correct structure to rebuilt the oracles

    label_data = [ord(ms_oracle.levels[level].objects[i].label) - prm.LETTER_DIFF
                  for i in range(len(ms_oracle.levels[level].objects))]

    ms_oracle.levels[level].iterator = len(ms_oracle.levels[level].concat_obj.concat_labels)
    ms_oracle.levels[level].shift = len(ms_oracle.levels[level].oracle.data) - len(
        ms_oracle.levels[level].concat_obj.concat_labels) - 1
    ms_oracle.levels[level].update_oracle(label_data[ms_oracle.levels[level].iterator + ms_oracle.levels[level].shift])
    ms_oracle.levels[level].actual_char = \
        ms_oracle.levels[level].oracle.data[ms_oracle.levels[level].shift + ms_oracle.levels[level].iterator + 1]
    ms_oracle.levels[level].data_length = len(ms_oracle.levels[level].formal_diagram.material_lines[0])
    ms_oracle.levels[level].objects = ms_oracle.levels[level].objects[ms_oracle.levels[level].shift:]
    ms_oracle.levels[level].actual_object = ms_oracle.levels[level].objects[ms_oracle.levels[level].iterator]

    ms_oracle.levels[level].formal_diagram.update(ms_oracle, level)
    ms_oracle.levels[level].formal_diagram_graph.update(ms_oracle, level)

    return 1


#=======================================
# PROHIBITIVE RULES

# RULE 4: (ab)(a + b => (ab)(ab
def validated_hypothesis(ms_oracle, level):
    """ Compare the concatenated object concat_obj of unstructured char in the actual level plus the actual_char, with
    the already seen objects in the past that begins with the same concat_obj. If the strings are equals, hypothesis
     from the past are validated and there should be no structuration right now because this is middle of the creation
     of an already known object of upper level. The function returns 1 then, 0 otherwise."""
    f_oracle = ms_oracle.levels[level].oracle
    link = ms_oracle.levels[level].link
    actual_char = ms_oracle.levels[level].actual_char
    actual_char_ind = ms_oracle.levels[level].actual_char_ind
    if len(f_oracle.data) > 2 and f_oracle.sfx[actual_char_ind - 1] != 0 \
            and f_oracle.data[f_oracle.sfx[actual_char_ind - 1] + 1] == actual_char \
            and len(link) > f_oracle.sfx[actual_char_ind - 1] + 1 \
            and link[f_oracle.sfx[actual_char_ind - 1]] == link[f_oracle.sfx[actual_char_ind - 1] + 1]:
        return 1
    return 0


def rule_4_not_validated_hypothesis(ms_oracle, level):
    """ This function compute the previous function validated hypothesis and returns the opposite result."""
    return abs(1 - validated_hypothesis(ms_oracle, level))


# RULE 5: (ab)(a + a => (ab)(aa // is a "or"
# RULEb: (ab)(a + a => (aba)(a
def rule_5_regathering_after(ms_oracle, level):
    """ The function returns 1 if the length of the string corresponding to  the concatenated object that are not
    structured in the actual level is higher than one. It returns 0 if the length of the string is equal or less than
    one."""
    if len(ms_oracle.levels[level].concat_obj.concat_labels) > 1:
        return 1
    return 0

def rule_5b_regathering_before():
    # TODO: à implémenter
    return 1


#================================
#AMBIVALENT RULES

# RULE 6a (lower boundary) : |(a...b + a| < low_bound => (a...ba
# RULE 6b (higher boundary) : |(a...b + c| > high_bound => (a...b)(c
def rule_6a_low_bound(ms_oracle, level):
    concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
    low_bound=lower_bound_rule6
    if len(concat_obj) < low_bound:
        return 0
    return 1


def rule_6b_high_bound(ms_oracle, level):
    concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
    high_bound=higher_bound_rule6
    if len(concat_obj) >= high_bound:
        return 1
    return 0


# RULE 7 (mean word length) : with A the length of the first concatenated word
# RULE 7a: |(a...b + a| < A/2 => (a...ba
# RULE 7b: |(a...b + c| > A + A/2 => (a...b)(c
def compute_length(ms_oracle, level):
    f_oracle = ms_oracle.levels[level].oracle
    a = f_oracle
    # TODO: à implémenter
    return 2


def rule_7a_mean_word_length_low(ms_oracle, level):
    concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
    f_oracle = ms_oracle.levels[level].oracle
    length = compute_length(f_oracle)
    if len(concat_obj) < length/2:
        return 0
    return 1


def rule_7b_mean_word_length_high(ms_oracle, level):
    concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
    f_oracle = ms_oracle.levels[level].oracle
    length = compute_length(f_oracle)
    if len(concat_obj) > (3*length)/2:
        return 1
    return 0


def rule_8a_repetition_paradigm_noseg(ms_oracle, level):
    concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
    f_oracle = ms_oracle.levels[level].oracle
    actual_char_ind = ms_oracle.levels[level].actual_char_ind
    if len(f_oracle.data) > 2 and len(concat_obj) > 0 and \
            f_oracle.data[actual_char_ind - 1] == f_oracle.data[actual_char_ind]:
        return 0
    return 1


def rule_8b_repetition_paradigm_seg(ms_oracle, level):
    concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
    f_oracle = ms_oracle.levels[level].oracle
    actual_char_ind = ms_oracle.levels[level].actual_char_ind
    if len(f_oracle.data) > 3 and len(concat_obj) > 1 and \
            f_oracle.data[actual_char_ind - 2] == f_oracle.data[actual_char_ind - 1] and \
            f_oracle.data[actual_char_ind - 1] != f_oracle.data[actual_char_ind]:
        return 1
    return 0

rule_tab = [[rule_1_similarity_word, rule_2_existing_object, rule_3_recomputed_object, 0, 0, rule_6b_high_bound, rule_7b_mean_word_length_high, rule_8b_repetition_paradigm_seg],
            [0, 0, 0, rule_4_not_validated_hypothesis, rule_5_regathering_after, rule_6a_low_bound, rule_7a_mean_word_length_low, rule_8a_repetition_paradigm_noseg]]

