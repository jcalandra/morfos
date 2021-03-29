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
            and len(link) > f_oracle.sfx[actual_char_ind - 1] + 2\
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
            if alignements.scheme_alignment(history_next[i][1], concat_obj, matrix)[0]: #and  \
                    #alignements.scheme_alignement(history_next[i][1], concat_obj + chr(actual_char + letter_diff), matrix)[0] == 0:
                return 1
    else:
        for i in range(len(history_next)):
            if history_next[i][1] == concat_obj:
                return 1
    return 0


def rule_4_recomputed_object_old(oracles, level, data_length, actual_char_ind):
    """ This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with substrings of objects of the upper level stocked in the tab history_next[]. If the strings are similar, the
    algorithm goes back to the similar state in the past, structure and recompute the oracles and other structures."""
    # allocation of structures of actual level
    f_oracle = oracles[1][level][0]
    link = oracles[1][level][1]
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    nb_elements = len(concat_obj)

    # Comparisons between concat_obj and the string starting from the suffix of the first char of concat_obj
    # if there is only one character in concat_obj, that is already seen, it's rule 1
    if nb_elements <= 1:
        return 0

    for i in range(nb_elements):
        # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
        if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + i] \
                != f_oracle.data[actual_char_ind - nb_elements + i]:
            return 0

    # if the actual concat_obj is not the longest common string :
    if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements] == f_oracle.data[actual_char_ind]:
        return 0

    if len(oracles[1]) > level + 1:

        # allocation of structures of level sup
        f_oracle_sup = oracles[1][level + 1][0]
        link_sup = oracles[1][level + 1][1]
        history_next_sup = oracles[1][level + 1][2]
        concat_obj_sup = oracles[1][level + 1][3]

        real_ind = link[f_oracle.sfx[actual_char_ind - nb_elements]]
        real_value = f_oracle_sup.data[real_ind]
        history_k = real_value - 1

        # if concat_obj corresponds to an already known object, return 0.
        if history_next[real_value - 1][1] == concat_obj:
            return 0

        # Structuring.
        # Modification of the structures if they exist :
        # actual level : link, history_next
        # next level : FO, history_next, link, concat_obj
        #
        # there is no need to modify next next level and so because there can not be any structuration between the two
        # nodes that are created in the next level as it's the separation of one new string into two new strings.

        # update of link
        for i in range(f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements, len(link)):
            link[i] = link[i] + 1

        # update of history_next
        j = 0
        nb_node = 0
        letter = ord(history_next[history_k][0])
        history_temp = history_next[history_k]
        history_next.pop(history_k)
        while history_temp[1][j] != concat_obj[0]:
            j += 1
        if j > 0:
            history_element = (chr(letter), history_temp[1][0:j])
            history_next.insert(history_k, history_element)
            letter += 1
            history_k += 1
            nb_node += 1
        history_element = (chr(letter), history_temp[1][j:j + len(concat_obj)])
        history_next.insert(history_k, history_element)
        letter += 1
        history_k += 1
        nb_node += 1
        if j + len(concat_obj) < len(history_temp[1]):
            history_element = (chr(letter), history_temp[1][j + len(concat_obj):])
            history_next.insert(history_k, history_element)
            letter += 1
            history_k += 1
            nb_node += 1
        for i in range(history_k, len(history_next)):
            new_el = (chr(letter), history_next[i][1])
            history_next[i] = new_el
            letter = letter + 1

        # update of the whole FO at next level
        new_fo_sup = oracle_mso.create_oracle('f')
        for i in range(1, real_ind):
            new_state = f_oracle_sup.data[i]
            new_fo_sup.add_state(new_state)
        for i in range(nb_node):
            history_k = f_oracle_sup.data[real_ind] + i
            new_fo_sup.add_state(history_k)
        for i in range(real_ind + 1, len(f_oracle_sup.data)):
            if f_oracle_sup.data[i] < len(history_next) - 1:
                new_state = f_oracle_sup.data[i]
            else:
                new_state = f_oracle_sup.data[i] + nb_node - 1
            new_fo_sup.add_state(new_state)
        oracles[1][level + 1][0] = new_fo_sup

        # update of the formal diagram at next level
        formal_diagram_sup = []
        formal_diagram_init(formal_diagram_sup, data_length, oracles, level)
        for i in range(2, len(new_fo_sup.data)):
            actual_char = new_fo_sup.data[i]
            formal_diagram_update(formal_diagram_sup, data_length, actual_char, i, oracles, level)
        oracles[1][level + 1][4] = formal_diagram_sup

        # update of link_sup and history_next_sup if necessary
        if len(link_sup) >= real_ind + 1:
            history_next_sup_value = oracles[1][level + 1][0].data[real_value - 1]
            link_temp = link_sup[real_ind]
            new_letter = history_next_sup[history_next_sup_value][0]
            string = history_next_sup[history_next_sup_value][1]
            for i in range(nb_node - 1):
                link_sup.insert(real_ind + i + 1, link_temp)
                string += chr(new_fo_sup.data[real_ind + i + 1] + letter_diff)
                new_hns = (new_letter, string)
                history_next_sup[history_next_sup_value] = new_hns
            for i in range(history_next_sup_value, len(history_next_sup)):
                new_letter = history_next_sup[i][0]
                old_string = history_next_sup[i][1]
                string = ''
                for k in range(len(old_string)):
                    string += chr(ord(old_string[k]) + nb_node - 1)
                new_hns = (new_letter, string)
                history_next_sup[i] = new_hns
            new_concat_obj_sup = ''

        else:
            new_concat_obj_sup = concat_obj_sup
        # update of concat_obj_sup if needed
        for i in range(len(concat_obj_sup)):
            new_concat_obj_sup += chr(new_fo_sup.data[len(new_fo_sup.data) - len(concat_obj_sup) + i] + letter_diff)
        oracles[1][level + 1][3] = new_concat_obj_sup
    return 1


def rule_4_recomputed_object_ok(oracles, level, actual_char_ind, str_obj, k, level_max, end_mk):
    """This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with substrings of objects of the upper level stocked in the tab history_next[]. If the strings are similar,
     the previous recognized string is structured and the algorithm rebuild the different FOs and structures back to
     this state and returns 1, otherwise returns 0."""
    # allocation of structures of actual level
    f_oracle = oracles[1][level][0]
    link = oracles[1][level][1]
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    nb_elements = len(concat_obj)

    # if there is only one character in concat_obj, that is already seen, it's rule 1
    if nb_elements <= 1:
        return 0, str_obj

    # if the longest similar suffix is not an adequate value
    if f_oracle.sfx[actual_char_ind - nb_elements] is None or f_oracle.sfx[actual_char_ind - nb_elements] == 0 or \
            f_oracle.sfx[actual_char_ind - nb_elements] == actual_char_ind - nb_elements - 1:
        return 0, str_obj

    # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
    if ALIGNEMENT_rule4:
        sub_suffix = ""
        for j in range(nb_elements):
            sub_suffix += chr(f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + j] + letter_diff)
            # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
        if alignements.scheme_alignment(sub_suffix, concat_obj, oracles[1][level - 1][6])[0] == 0:
            return 0, str_obj

    else:
        for j in range(nb_elements):
            if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + j] \
                    != f_oracle.data[actual_char_ind - nb_elements + j]:
                return 0, str_obj

    # if the the longest similar suffix is constitued of different materials
    for i in range(1, nb_elements):
        if link[f_oracle.sfx[actual_char_ind - nb_elements] + i - 1] != link[f_oracle.sfx[actual_char_ind - nb_elements] + i]:
            return 0, str_obj

    # if the the longest similar suffix does not begin the corresponding material
    if link[f_oracle.sfx[actual_char_ind - nb_elements]] == link[f_oracle.sfx[actual_char_ind - nb_elements] - 1]:
        return 0, str_obj

    # if the actual concat_obj is not the longest common string :
    if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements] == f_oracle.data[actual_char_ind]:
        return 0, str_obj

    if len(oracles[1]) > level + 1:

        # allocation of structures of level sup
        f_oracle_sup = oracles[1][level + 1][0]

        real_ind = link[f_oracle.sfx[actual_char_ind - nb_elements]]
        real_value = f_oracle_sup.data[real_ind]

        # if concat_obj corresponds to an already known object, return 0.
        if ALIGNEMENT_rule4:
            if alignements.scheme_alignment(history_next[real_value - 1][1], concat_obj, oracles[1][level - 1][6])[0] == 1:
                return 0, str_obj
        else:
            if history_next[real_value - 1][1] == concat_obj:
                return 0, str_obj

            if link[f_oracle.sfx[actual_char_ind - nb_elements]] != \
                    link[f_oracle.sfx[actual_char_ind - nb_elements] - 1] and \
                    link[f_oracle.sfx[actual_char_ind - nb_elements]] !=\
                    link[f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements + 1]:
                return 0, str_obj

    # else, we are in the required conditions and we rebuild the oracles
    # We go back to the new already-seen state
    to_struct = 0
    new_ind_p1 = -1
    level_up = level
    level_tmp = -1
    ind = f_oracle.sfx[actual_char_ind - nb_elements] - 1
    k_init = ind
    frame_level = level
    while frame_level > 0:
        k_init = oracles[1][frame_level - 1][1].index(k_init)
        while len(oracles[1][frame_level - 1][1]) > k_init + 1 and \
                oracles[1][frame_level - 1][1][k_init] == oracles[1][frame_level - 1][1][k_init + 1]:
            k_init += 1
        frame_level -= 1

    # compute the string that has to be rebuilt at actual level before going back to lower levels
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

    # for each level n superior or equal to actual level:
    while len(oracles[1]) > level_up != level_tmp:
        new_fo = oracle_mso.create_oracle('f')

        # f_oracle update
        i = 1
        while i < ind + 1:
            new_state = oracles[1][level_up][0].data[i]
            new_fo.add_state(new_state)
            i += 1

        # formal diagram update
        data_length = len(oracles[1][level_up][4][0])
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
                if new_ind == new_ind_p1:
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
            # concat_obj update
            for j in range(nb_elements):
                actual_char = f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + j]
                element = chr(actual_char + letter_diff)
                oracles[1][level_up][3] += element
                new_state = oracles[1][level_up][0].data[i + j]
                new_fo.add_state(new_state)
                # formal diagram update
                char_ind = ind + j + 1
                formal_diagram_update(oracles[1][level_up][4], data_length, actual_char, char_ind, oracles,
                                      level_up)
                print_formal_diagram_update(oracles[1][level_up][5], level_up, oracles[1][level_up][4], data_length)

        new_ind = max(oracles[1][level_up][1])
        oracles[1][level_up][0] = new_fo

        # next level
        level_tmp = level_up
        if level_up < len(oracles[1]) - 1:
            next_ind = max(oracles[1][level_up + 1][0].data[:new_ind + 1])
            len_max = len(oracles[1][level_up][2])
            for j in range(len_max - next_ind):
                # history_next update
                oracles[1][level_up][2].pop(len(oracles[1][level_up][2]) - 1)
                # matrix update
                oracles[1][level_up][6][0] = oracles[1][level_up][6][0][:-1]
                oracles[1][level_up][6][1].pop()
                for mat_line in range(len(oracles[1][level_up][6][1])):
                    oracles[1][level_up][6][1][mat_line].pop()

            if len(oracles[1][level_up][1]) > 1 and level_up == level and to_struct:
                cmp = 1
                while oracles[1][level_up][1][-1] == oracles[1][level_up][1][-1 - cmp]:
                    cmp += 1
                new_mat = (oracles[1][level_up][2][-1][0], oracles[1][level_up][2][-1][1][:cmp])
                oracles[1][level_up][2][-1] = new_mat
                # TODO : modifier la valeur adéquate dans la matrice d'autosimilarité

            ind = new_ind
            level_up = level_up + 1

    # Then go back to the main loop of the structuring function with the correct structure to rebuilt the oracles
    return 1, str_obj


def rule_4_recomputed_object(oracles, level, actual_char_ind, str_obj, k, level_max, end_mk):
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
    if f_oracle.sfx[actual_char_ind - nb_elements] is None or f_oracle.sfx[actual_char_ind - nb_elements] == 0 or \
            f_oracle.sfx[actual_char_ind - nb_elements] == actual_char_ind - nb_elements - 1:
        return 0, str_obj

    # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
    if ALIGNEMENT_rule4:
        for j in range(nb_elements):
            sub_suffix += chr(f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + j] + letter_diff)
            # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
        if alignements.scheme_alignment(sub_suffix, concat_obj, oracles[1][level - 1][6])[0] == 0:
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
                                         oracles[1][level - 1][6])[0] == 1:
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
                    history_next[real_value - 1][1], concat_obj, oracles[1][level - 1][6])[0] == 1 or \
                    alignements.scheme_alignment(
                    history_next[real_value - 1][1], sub_suffix, oracles[1][level - 1][6])[0] == 1:
                return 0, str_obj
        else:
            if history_next[real_value - 1][1] == concat_obj:
                return 0, str_obj

            if link[f_oracle.sfx[actual_char_ind - nb_elements]] != \
                    link[f_oracle.sfx[actual_char_ind - nb_elements] - 1] and \
                    link[f_oracle.sfx[actual_char_ind - nb_elements]] !=\
                    link[f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements + 1]:
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
    k_init = ind
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
                print("oui")
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
                str_obj = str_obj[(ind_init - ind_fo_init):]

                # history next
                while len(oracles[1][level_up][2]) > max(oracles[1][level_up][1]):
                    oracles[1][level_up][2].pop()
                    oracles[1][level_up][6][0] = oracles[1][level_up][6][0][:-1]
                    oracles[1][level_up][6][1].pop()
                    for mat_line in range(len(oracles[1][level_up][6][1])):
                        oracles[1][level_up][6][1][mat_line].pop()
                print("len history next", len(oracles[1][level_up][2]))
                print("max link", max(oracles[1][level_up][1]))

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
            if level_up == level:
                print("max link", max(oracles[1][level_up][1]))
                print("len history next", len(oracles[1][level_up][2]))
                print("len matrix next 0", len(oracles[1][level_up][6][0]))

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

        print(len(oracles[1][level][6][0]))
        as_mso.structure(
            oracles[1][level][2], to_struct_obj, oracles, level, oracles[1][level][1], data_length, level_max, 0)
        print(len(oracles[1][level][6][0]))
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
