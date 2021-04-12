import oracle_mso
import alignements
import algo_segmentation_mso as as_mso
from formal_diagram_mso import *

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


RULE_1 = prm.RULE_1
RULE_2 = prm.RULE_2
RULE_3 = prm.RULE_3
RULE_4 = prm.RULE_4
RULE_5 = prm.RULE_5
ALIGNEMENT_rule3 = prm.ALIGNEMENT_rule3
ALIGNEMENT_rule4 = prm.ALIGNEMENT_rule4

letter_diff = prm.LETTER_DIFF


def rule_1_similarity(f_oracle, actual_char_ind):
    """ Look the suffix of actual char which is at 'actual_char_ind'. Return 1 if the actual_char has already been seen,
     meaning its suffix is not 0, otherwise the function returns 0, meaning it's a new material."""
    if f_oracle.sfx[actual_char_ind] != 0:
        return 1
    return 0


def validated_hypothesis(f_oracle, link, actual_char, actual_char_ind):
    """ Compare the concatenated object concat_obj of unstructured char in the actual level plus the actual_char, with
    the already seen objects in the past that begins with the same concat_obj. If the strings are equals, hypothesis
     from the past are validated and there should be no structuration right now because this is middle of the creation
     of an already known object of upper level. The function returns 1 then, 0 otherwise."""
    if len(f_oracle.data) > 2 and f_oracle.sfx[actual_char_ind - 1] != 0 \
            and f_oracle.data[f_oracle.sfx[actual_char_ind - 1] + 1] == actual_char \
            and len(link) > f_oracle.sfx[actual_char_ind - 1] + 1\
            and link[f_oracle.sfx[actual_char_ind - 1]] == link[f_oracle.sfx[actual_char_ind - 1] + 1]:
        return 1
    return 0


def rule_2_not_validated_hypothesis(f_oracle, link, actual_char, actual_char_ind):
    """ This function compute the previous function validated hypothesis and returns the opposite result."""
    return abs(1 - validated_hypothesis(f_oracle, link, actual_char, actual_char_ind))


def rule_3_existing_object(history_next, concat_obj, actual_char, matrix):
    """ This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with objects of the upper level stocked in the tab history_next[]. If the strings are similar, returns 1. Otherwise
    the function returns 0."""
    if ALIGNEMENT_rule3:
        for i in range(len(history_next)):
            if alignements.scheme_alignment(history_next[i][1], concat_obj, matrix)[0] and  \
                    alignements.scheme_alignment(
                        history_next[i][1], concat_obj + chr(actual_char + letter_diff), matrix)[0] == 0:
                return 1
    else:
        for i in range(len(history_next)):
            if history_next[i][1] == concat_obj:
                return 1
    return 0


def rule_4_recomputed_object(oracles, matrix, level, actual_char_ind, str_obj, k, level_max, end_mk):
    """ This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with substrings of objects of the upper level stocked in the tab history_next[]. If the strings are similar, the
    algorithm goes back to the similar state in the past, structure and recompute the oracles and other structures."""
    # allocation of structures of actual level
    f_oracle = oracles[1][level][0]
    link = oracles[1][level][1].copy()
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    nb_elements = len(concat_obj)
    sub_suffix = ""

    # if there is only one character in concat_obj, that is already seen, it's rule 1
    if nb_elements <= 1:
        return 0, str_obj

    # if the longest similar suffix is not an adequate value
    if f_oracle.sfx[actual_char_ind - nb_elements] is None or f_oracle.sfx[actual_char_ind - nb_elements] == 0 or\
            f_oracle.sfx[actual_char_ind - nb_elements] == actual_char_ind - nb_elements - 1:
        return 0, str_obj

    # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
    if ALIGNEMENT_rule4:
        for j in range(nb_elements):
            sub_suffix += chr(f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + j] + letter_diff)
            # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
        if alignements.scheme_alignment(sub_suffix, concat_obj, matrix)[0] == 0:
            return 0, str_obj

    else:
        for j in range(nb_elements):
            if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + j] \
                    != f_oracle.data[actual_char_ind - nb_elements + j]:
                return 0, str_obj

    # if the the longest similar suffix is constitued of different materials
    for i in range(1, nb_elements):
        if len(link) < f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements + 1 or \
                link[f_oracle.sfx[actual_char_ind - nb_elements] + i - 1] !=\
                link[f_oracle.sfx[actual_char_ind - nb_elements] + i]:
            return 0, str_obj

    # if the longest similar suffix has only one caracter before it and RULE 5 is activated
    if RULE_5:
        if link[f_oracle.sfx[actual_char_ind - nb_elements]] ==\
                link[f_oracle.sfx[actual_char_ind - nb_elements] - 1] \
                and link[f_oracle.sfx[actual_char_ind - nb_elements] - 1] !=\
                link[f_oracle.sfx[actual_char_ind - nb_elements] - 2]:
            return 0, str_obj

    # if the actual concat_obj is not the longest common string :
    if ALIGNEMENT_rule4:
        if alignements.scheme_alignment(sub_suffix, concat_obj + chr(f_oracle.data[actual_char_ind] + letter_diff),
                                         matrix)[0] == 1:
            return 0, str_obj
    else:
        if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements] == f_oracle.data[actual_char_ind]:
            return 0, str_obj

    if len(oracles[1]) > level + 1:

        # allocation of structures of level sup
        f_oracle_sup = oracles[1][level + 1][0]
        real_ind = link[f_oracle.sfx[actual_char_ind - nb_elements]]
        real_value = f_oracle_sup.data[real_ind]

        # if concat_obj corresponds to an already known object, return 0.
        if ALIGNEMENT_rule4:
            if alignements.scheme_alignment(
                    history_next[real_value - 1][1], concat_obj, matrix)[0] == 1 or \
                    alignements.scheme_alignment(
                    history_next[real_value - 1][1], sub_suffix, matrix)[0] == 1:
                return 0, str_obj
        else:
            if history_next[real_value - 1][1] == concat_obj:
                return 0, str_obj

            if link[f_oracle.sfx[actual_char_ind - nb_elements]] != \
                    link[f_oracle.sfx[actual_char_ind - nb_elements] - 1] and \
                    link[f_oracle.sfx[actual_char_ind - nb_elements]] !=\
                    link[f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements]:
                return 0, str_obj

    # else, we are in the required conditions and we rebuild the oracles
    # we go back to the new already-seen state
    data_length = len(oracles[1][level][4][0])
    to_struct = 0
    to_struct_obj = ''

    frame_level = level
    level_up = level
    level_tmp = -1

    ind = f_oracle.sfx[actual_char_ind - nb_elements] - 1
    ind_init = ind
    new_ind_p1 = -1
    ind_fo_init = 1
    ind_to_struct = 0

    # compute the string that has to be fully rebuilt at actual level before going back to lower levels
    if actual_char_ind > len(str_obj) + k:
        str_obj = ""
        for i in range(ind + 1, len(f_oracle.data)):
            str_obj += chr(f_oracle.data[i] + letter_diff)
    else:
        if ind >= k:
            str_obj = str_obj[ind - k:]
        else:
            str_2apn = ""
            for i in range(ind + 1, k + 1):
                str_2apn += chr(f_oracle.data[i] + letter_diff)
            str_obj = str_2apn + str_obj

    # each level level_up superior or equal to actual level is recomputed
    while len(oracles[1]) > level_up != level_tmp:
        new_fo = oracle_mso.create_oracle('f')

        # f_oracle update
        i = 1
        while i < ind + 1:
            new_state = oracles[1][level_up][0].data[i]
            new_fo.add_state(new_state)
            i += 1

        # compute k_init according to the adequate frame at level 0 for formal diagram representation
        k_init = ind
        frame_level = level_up
        while frame_level > 0:
            k_init = oracles[1][frame_level - 1][1].index(k_init)
            while len(oracles[1][frame_level - 1][1]) > k_init + 1 and \
                    oracles[1][frame_level - 1][1][k_init] == oracles[1][frame_level - 1][1][k_init + 1]:
                k_init += 1
            frame_level -= 1

        # formal diagram update
        for j in range(len(oracles[1][level_up][4])):
            for fd_ind in range(k_init, data_length):
                oracles[1][level_up][4][j][fd_ind] = 1
        print_formal_diagram_update(oracles[1][level_up][5], level_up, oracles[1][level_up][4], data_length)

        # link update
        if len(oracles[1][level_up][1]) > ind:
            new_ind = oracles[1][level_up][1][ind]
            seg = 0
            oracles[1][level_up][3] = ''
            if len(oracles[1][level_up][1]) > ind + 1:
                new_ind_p1 = oracles[1][level_up][1][ind + 1]
                if level_up == level and new_ind == new_ind_p1:
                    to_struct = 1
        else:
            new_ind = max(oracles[1][level_up][1])
            seg = 1
        while i < len(oracles[1][level_up][1]):
            oracles[1][level_up][1].pop(i)
        if level_up != level:
            tmp_concat_obj = ''
            if seg == 0 and len(oracles[1][level_up][1]) > 1 and new_ind == new_ind_p1:
                while oracles[1][level_up][1][len(oracles[1][level_up][1]) - 1] == new_ind:
                    tmp_concat_obj = chr(oracles[1][level_up][0].data[len(oracles[1][level_up][1]) - 1] + letter_diff) \
                                     + tmp_concat_obj
                    oracles[1][level_up][1].pop(len(oracles[1][level_up][1]) - 1)

                    # concat_obj update
                oracles[1][level_up][3] = tmp_concat_obj

            elif seg == 1:
                oracles[1][level_up][3] = \
                    oracles[1][level_up][3][:len(new_fo.data) - len(oracles[1][level_up][1])]

        else:
            if to_struct and len(oracles[1][level_up][1]) > 1:
                # link update and computation of to_struct_obj
                while oracles[1][level_up][1][len(oracles[1][level_up][1]) - 1] == new_ind:
                    to_struct_obj = chr(oracles[1][level_up][0].data[len(oracles[1][level_up][1]) - 1] + letter_diff) \
                        + to_struct_obj
                    oracles[1][level_up][1].pop(len(oracles[1][level_up][1]) - 1)
                    ind_to_struct += 1

                new_fo = oracle_mso.create_oracle('f')
                # f_oracle update
                while ind_fo_init < ind_init + 1 - ind_to_struct:
                    new_state = oracles[1][level_up][0].data[ind_fo_init]
                    new_fo.add_state(new_state)
                    ind_fo_init += 1

                # formal diagram update
                frame_level = level_up
                former_k_init = ind_init
                k_init = ind_init - ind_to_struct
                while frame_level > 0:
                    k_init = oracles[1][frame_level - 1][1].index(k_init)
                    while len(oracles[1][frame_level - 1][1]) > k_init + 1 and \
                            oracles[1][frame_level - 1][1][k_init] == oracles[1][frame_level - 1][1][k_init + 1]:
                        k_init += 1
                    frame_level -= 1

                for j in range(len(oracles[1][level_up][4])):
                    for fd_ind in range(k_init, former_k_init):
                        oracles[1][level_up][4][j][fd_ind] = 1
                print_formal_diagram_update(oracles[1][level_up][5], level_up, oracles[1][level_up][4], data_length)

                # str_obj
                #str_obj = str_obj[ind_to_struct - len(concat_obj):]  # str_obj[(ind_init - ind_fo_init) - 1:]

                # history next
                while len(oracles[1][level_up][2]) > max(oracles[1][level_up][1]):
                    oracles[1][level_up][2].pop()
                    oracles[1][level_up][6][0] = oracles[1][level_up][6][0][:-1]
                    oracles[1][level_up][6][1].pop()
                    for mat_line in range(len(oracles[1][level_up][6][1])):
                        oracles[1][level_up][6][1][mat_line].pop()

        new_ind = max(oracles[1][level_up][1])
        oracles[1][level_up][0] = new_fo

        # next level
        level_tmp = level_up
        if level_up < len(oracles[1]) - 1:
            next_ind = max(oracles[1][level_up + 1][0].data[:new_ind + 1])
            len_max = len(oracles[1][level_up][2])
            for j in range(len_max - next_ind):
                # history_next update
                oracles[1][level_up][2].pop()
                # matrix update
                oracles[1][level_up][6][0] = oracles[1][level_up][6][0][:-1]
                oracles[1][level_up][6][1].pop()
                for mat_line in range(len(oracles[1][level_up][6][1])):
                    oracles[1][level_up][6][1][mat_line].pop()

            ind = new_ind
            level_up = level_up + 1

    # if necessary, compute to_struct_obj and structure
    if to_struct:
        for j in range(ind_to_struct):
            char_ind = ind_fo_init + j
            new_state = f_oracle.data[char_ind]
            oracles[1][level][0].add_state(new_state)
            oracles[1][level][3] += to_struct_obj[j]
            # formal diagram update at initial level
            formal_diagram_update(oracles[1][level][4], data_length, new_state, char_ind, oracles, level)
            print_formal_diagram_update(oracles[1][level][5], level, oracles[1][level][4], data_length)
        if level == 0:
            as_mso.structure(
                oracles[1][level][2], oracles[1][level][7], to_struct_obj, oracles, level, oracles[1][level][1], data_length, level_max, end_mk)
        else:
            as_mso.structure(
                oracles[1][level][2], oracles[1][level - 1][6], to_struct_obj, oracles, level, oracles[1][level][1],
                data_length, level_max, end_mk)
        oracles[1][level][3] = ""

    # concat_obj update at initial level
    for j in range(nb_elements):
        char_ind = ind_init + j + 1
        new_state = f_oracle.data[char_ind]
        element = chr(new_state + letter_diff)
        oracles[1][level][3] += element
        oracles[1][level][0].add_state(new_state)
        # formal diagram update at initial level
        formal_diagram_update(oracles[1][level][4], data_length, new_state, char_ind, oracles, level)
        print_formal_diagram_update(oracles[1][level][5], level, oracles[1][level][4], data_length)

    # Then go back to the main loop of the structuring function with the correct structure to rebuilt the oracles
    return 1, str_obj


def rule_5_regathering(concat_obj):
    """ The function returns 1 if the length of the string corresponding to  the concatenated object that are not
    structured in the actual level is higher than one. It returns 0 if the length of the string is equal or less than
    one."""
    if len(concat_obj) > 1:
        return 1
    return 0
