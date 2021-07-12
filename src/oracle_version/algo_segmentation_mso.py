import mso
import parameters as prm
import formal_diagram_mso as fd_mso
import segmentation_rules_mso
import similarity_rules

# In this file is defined the main loop for the algorithm at symbolic scale
# structring test function according to rules (rules_parametrization) and similarity test function
# (char_next_level_similarity) are also defined here

letter_diff = prm.LETTER_DIFF
wait = 0
processing = prm.processing


# ============================================ SEGMENTATION FUNCTION ===================================================
def rules_parametrization(f_oracle, matrix, actual_char, actual_char_ind, link, oracles, level, i, k, history_next,
                          concat_obj, formal_diagram, formal_diagram_graph, str_obj, input_data, level_max, end_mk):
    """ Structuring test function: if one test is validated, there is structuration."""
    potential_obj = None
    if segmentation_rules_mso.RULE_1:
        test_1 = segmentation_rules_mso.rule_1_similarity(f_oracle, actual_char_ind)
    else:
        test_1 = 1
    if segmentation_rules_mso.RULE_2:
        test_2 = segmentation_rules_mso.rule_2_not_validated_hypothesis(f_oracle, link, actual_char, actual_char_ind)
    else:
        test_2 = 1
    if not segmentation_rules_mso.RULE_1 and not segmentation_rules_mso.RULE_2:
        test_1 = 0
        test_2 = 0
    if segmentation_rules_mso.RULE_4:
        test_4, potential_obj = segmentation_rules_mso.rule_4_recomputed_object(
            oracles, matrix, level, actual_char_ind, str_obj, k, level_max, end_mk)
    else:
        test_4 = 0
    if segmentation_rules_mso.RULE_3 and test_4 == 0:
        test_3 = segmentation_rules_mso.rule_3_existing_object(history_next, concat_obj, actual_char, matrix)
    else:
        test_3 = 0
    if segmentation_rules_mso.RULE_5:
        test_5 = segmentation_rules_mso.rule_5_regathering(concat_obj)
    else:
        test_5 = 1

    if test_4:
        f_oracle = oracles[1][level][0]
        link = oracles[1][level][1]
        history_next = oracles[1][level][2]
        concat_obj = oracles[1][level][3]
        formal_diagram = oracles[1][level][4]

        str_obj = potential_obj
        input_data = [ord(potential_obj[i]) - letter_diff for i in range(len(potential_obj))]

        i = len(concat_obj)
        k = len(f_oracle.data) - len(concat_obj) - 1
        f_oracle.add_state(input_data[i])
        actual_char = f_oracle.data[k + i + 1]
        data_length = len(formal_diagram[0])
        fd_mso.formal_diagram_update(formal_diagram, data_length, actual_char, k + i + 1, oracles, level)
        oracles[1][level][5] = fd_mso.print_formal_diagram_update(
            formal_diagram_graph, level, formal_diagram, data_length)
        formal_diagram_graph = oracles[1][level][5]

    return test_1, test_2, test_3, test_4, test_5, i, k, actual_char, \
        f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, str_obj, input_data


def structure(history_next, matrix, concat_obj, oracles, level, link, data_length, level_max, end_mk):
    """ Function for the structuring operation and therfore the update of the structures at this level and next level"""
    # Labelling upper level string and updating the different structures
    new_char = similarity_rules.char_next_level_similarity(history_next, matrix, oracles[1][level][6], concat_obj)
    if len(oracles[1]) > level + 1:
        node = max(oracles[1][level][1]) + 1
    else:
        node = 1
    for ind in range(len(concat_obj)):
        link.append(node)

    # send to the next f_oracle the node corresponding to concat_obj
    fun_segmentation(oracles, new_char, data_length, level + 1, level_max, end_mk)
    return 0


# ================================= MAIN COGNITIVE ALGORITHM AT SYMBOLIC SCALE =========================================
def fun_segmentation(oracles, str_obj, data_length, level=0, level_max=-1, end_mk=0):
    """This function browses the string char and structure it at the upper level according to the rules that are applied
    by the extern user."""
    # end of the recursive loop
    if level > oracles[0] and end_mk == 1:
        return 0

    #  Initialisation of the structures
    if level > oracles[0]:
        if prm.verbose == 1:
            print("[INFO] CREATION OF NEW FO : LEVEL " + str(level) + "...")
        flag = 'f'

        f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix_next = \
            mso.structure_init(flag, level)

        oracles[0] = level
        level_max = level

        if level == 0 and processing == 'symbols':
            vec = [1]
            matrix = [chr(fd_mso.letter_diff + ord(str_obj[0])), [vec]]
            oracles[1].append([f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix_next, matrix])
        elif level > 0:
            matrix = oracles[1][level - 1][6]
            oracles[1].append([f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix_next])

    else:
        f_oracle = oracles[1][level][0]
        link = oracles[1][level][1]
        history_next = oracles[1][level][2]
        concat_obj = oracles[1][level][3]
        formal_diagram = oracles[1][level][4]
        formal_diagram_graph = oracles[1][level][5]
        matrix_next = oracles[1][level][6]
        if level > 0:
            matrix = oracles[1][level - 1][6]
        else:
            matrix = oracles[1][level][7]

    # Every new character is analysed.
    input_data = [ord(str_obj[ind_input]) - letter_diff for ind_input in range(len(str_obj))]
    level_wait = -1
    global wait
    k = len(f_oracle.data) - 1
    i = 0
    if prm.verbose == 1:
        print("[INFO] Process in level " + str(level) + "...")
    while i < len(str_obj):
        f_oracle.add_state(input_data[i])
        actual_char = f_oracle.data[k + i + 1]  # i_th parsed character
        actual_char_ind = k + i + 1

        if level == 0 and processing == 'symbols' and \
                actual_char > max([ord(matrix[0][ind]) for ind in range(len(matrix[0]))]):
            vec = [0 for ind_vec in range(len(matrix[0]))]
            vec.append(1)
            matrix[0] += chr(actual_char + fd_mso.letter_diff)
            matrix[1].append(vec)
            for ind_mat in range(len(matrix[1]) - 1):
                matrix[1][ind_mat].append(matrix[1][len(matrix[1]) - 1][ind_mat])

        # formal diagram is updated with the new char
        if actual_char_ind == 1:
            fd_mso.formal_diagram_init(formal_diagram, data_length, oracles, level)
        else:
            fd_mso.formal_diagram_update(formal_diagram, data_length, actual_char, actual_char_ind, oracles, level)

        oracles[1][level][5] = fd_mso.print_formal_diagram_update(
            formal_diagram_graph, level, formal_diagram, data_length)

        # First is the parametrisation of the rules according to the external settings.
        test_1, test_2, test_3, test_4, test_5, i, k, actual_char, f_oracle, link, history_next, concat_obj, \
            formal_diagram, formal_diagram_graph, str_obj, input_data = rules_parametrization(
                f_oracle, matrix, actual_char, actual_char_ind, link, oracles, level, i, k, history_next, concat_obj,
                formal_diagram, formal_diagram_graph, str_obj, input_data, level_max, end_mk)

        if level > 0 and end_mk == 1 and i < len(str_obj) - 1:
            end_mk = 0
            wait = 1
            level_wait = level

        # If the tests are positives, there is structuration.
        if ((test_1 and test_2) or (test_2 and test_3) or test_4) and test_5 and (end_mk == 0):
            # or (end_mk == 1 and len(concat_obj) != 0):
            structure(history_next, matrix, concat_obj, oracles, level, link, data_length, level_max, end_mk)
            if prm.verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            concat_obj = ''
        concat_obj = concat_obj + chr(actual_char + letter_diff)
        oracles[1][level][3] = concat_obj

        # Automatically structuring if this is the End Of String
        if (level == 0 and i == len(str_obj) - 1) or (wait == 1 and level == level_wait and i == len(str_obj) - 1):
            end_mk = 1
            wait = 0
            level_wait = -1
        if end_mk == 1:
            structure(history_next, matrix, concat_obj, oracles, level, link, data_length, level_max, end_mk)
            if prm.verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            concat_obj = ''
        oracles[1][level][3] = concat_obj
        i += 1
        if prm.verbose == 1:
            print("state number ", i, " in level ", level)

    return 1
