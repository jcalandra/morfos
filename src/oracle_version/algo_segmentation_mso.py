from rules_mso import *
import mso


# ================================================ SIMILARITY ==========================================================
def char_next_level_similarity(history_next, concat_obj):
    """ The function compare the actual new structured string with structured strings already seen before. For now,
    the strings have to be the exact sames to be considered as similar. The history_next tab is modified according to
    the results and the new string of upper level new_char is returned."""
    for i in range(len(history_next)):
        if len(concat_obj) == len(history_next[i][1]):
            j = 0
            while history_next[i][1][j] == concat_obj[j]:
                j = j + 1
                if j == len(history_next[i][1]):
                    new_char = history_next[i][0]
                    return new_char
    new_char = chr(97 + len(history_next))
    history_next.append((new_char, concat_obj))
    return new_char


# ============================================ SEGMENTATION FUNCTION ===================================================

def rules_parametrization(f_oracle, actual_char, actual_char_ind, link, oracles, level, i,
                          history_next, concat_obj, nb_elements, formal_diagram, formal_diagram_graph):
    if RULE_1:
        test_1 = rule_1_similarity(f_oracle, actual_char_ind)
    else:
        test_1 = 1
    if RULE_2:
        test_2 = rule_2_not_validated_hypothesis(f_oracle, link, actual_char, actual_char_ind)
    else:
        test_2 = 1
    if not RULE_1 and not RULE_2:
        test_1 = 0
        test_2 = 0
    if RULE_4:
        test_4 = rule_4_recomputed_object(oracles, level, actual_char_ind)
    else:
        test_4 = 0
    if RULE_3:
        test_3 = rule_3_existing_object(history_next, concat_obj)
    else:
        test_3 = 0
    if RULE_5:
        test_5 = rule_5_regathering(concat_obj)
    else:
        test_5 = 1

    if test_4:
        i = f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements - 1
        actual_char = f_oracle.data[i + 1]
        f_oracle = oracles[1][level][0]
        link = oracles[1][level][1]
        history_next = oracles[1][level][2]
        concat_obj = oracles[1][level][3]
        formal_diagram = oracles[1][level][4]
        data_length = len(formal_diagram[0])
        formal_diagram_update(formal_diagram, data_length, actual_char, i + 1, oracles, level)
        oracles[1][level][5] = print_formal_diagram_update(formal_diagram_graph, level, formal_diagram, data_length)
        formal_diagram_graph = oracles[1][level][5]
        f_oracle.add_state(actual_char)
    return test_1, test_2, test_3, test_4, test_5, \
        i, actual_char, f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph


def structure(history_next, concat_obj, oracles, level, link, data_length, level_max, end_mk):
    print("Structuring")
    # Labelling upper level string and updating the different structures
    new_char = char_next_level_similarity(history_next, concat_obj)
    if len(oracles[1]) > level + 1:
        node = len(oracles[1][level + 1][0].data)
    else:
        node = 1
    for ind in range(len(concat_obj)):
        link.append(node)

    # send to the next f_oracle the node corresponding to concat_obj
    fun_segmentation(oracles, new_char, data_length, level + 1, level_max, end_mk)
    return 0


def fun_segmentation(oracles, str_obj, data_length, level=0, level_max=-1, end_mk=0):
    """This function browses the string char and structure it at the upper level according to the rules that are applied
    by the extern user. It returns the structured char which is a tab of substring representing upper level object, the
    new string wew_char of upper level with adequated letters and the tab history[] of objects that are seen in this
    level."""
    # end of the recursive loop
    if level > oracles[0] and end_mk == 1:
        return 0

    #  Initialisation of the structures
    if level > oracles[0]:
        print("[INFO] CREATION OF NEW FO : LEVEL " + str(level) + "...")
        flag = 'f'

        f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph = \
            mso.structure_init(flag, level)
        oracles[1].append([f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph])

        oracles[0] = level
        level_max = level

    else:
        f_oracle = oracles[1][level][0]
        link = oracles[1][level][1]
        history_next = oracles[1][level][2]
        concat_obj = oracles[1][level][3]
        formal_diagram = oracles[1][level][4]
        formal_diagram_graph = oracles[1][level][5]

    # Every new character is analysed.
    input_data = [ord(str_obj[i]) - letter_diff for i in range(len(str_obj))]
    k = len(f_oracle.data) - 1
    i = 0
    while i < len(str_obj):
        print("[INFO] PROCESS IN LEVEL " + str(level))
        f_oracle.add_state(input_data[i])
        actual_char = f_oracle.data[k + i + 1]  # i_th parsed character
        actual_char_ind = k + i + 1
        nb_elements = len(concat_obj)
        print("Actual char processed is " + chr(actual_char + letter_diff))

        # formal diagram is updated with the new char
        if actual_char_ind == 1:
            formal_diagram_init(formal_diagram, data_length, oracles, level)
        else:
            formal_diagram_update(formal_diagram, data_length, actual_char, actual_char_ind, oracles, level)

        oracles[1][level][5] = print_formal_diagram_update(formal_diagram_graph, level, formal_diagram, data_length)

        # First is the parametrisation of the rules according to the external settings.
        test_1, test_2, test_3, test_4, test_5, i, actual_char, f_oracle, link, history_next, concat_obj, \
            formal_diagram, formal_diagram_graph = rules_parametrization(
                f_oracle, actual_char, actual_char_ind, link, oracles, level, i, history_next, concat_obj, nb_elements,
                formal_diagram, formal_diagram_graph)

        # If the tests are positives, there is structuration.
        if ((test_1 and test_2) or test_3 or test_4) and test_5 and \
                (end_mk == 0 or (end_mk == 1 and len(concat_obj) != 0)):
            structure(history_next, concat_obj, oracles, level, link, data_length, level_max, end_mk)
            print("[INFO] PROCESS IN LEVEL " + str(level))
            concat_obj = ''
        concat_obj = concat_obj + chr(actual_char + letter_diff)
        oracles[1][level][3] = concat_obj

        # Automatically structuring if this is the End Of String
        if level == 0 and i == len(str_obj) - 1:
            end_mk = 1
        if end_mk == 1:
            structure(history_next, concat_obj, oracles, level, link, data_length, level_max, end_mk)
            concat_obj = ''
        oracles[1][level][3] = concat_obj
        i += 1

    return 1
