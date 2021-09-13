from parameters import LETTER_DIFF, processing, verbose
import segmentation_rules_mso
import similarity_rules

import class_mso

# In this file is defined the main loop for the algorithm at symbolic scale
# structring test function according to rules (rules_parametrization) and similarity test function
# (char_next_level_similarity) are also defined here
wait = 0


# TODO: modifier les objets: un objet doit être une structure qui contient
#  - un label
#  - un ensemble de fonctions et les paramètres associés


# ============================================ SEGMENTATION FUNCTION ===================================================
def rules_parametrization(matrix, ms_oracle, level, i, k, str_obj, input_data, end_mk):
    """ Structuring test function: if one test is validated, there is structuration."""
    potential_obj = None
    if segmentation_rules_mso.RULE_1:
        test_1 = segmentation_rules_mso.rule_1_similarity(ms_oracle.levels[level].oracle,
                                                          ms_oracle.levels[level].actual_char_ind)
    else:
        test_1 = 1
    if segmentation_rules_mso.RULE_2:
        test_2 = segmentation_rules_mso.rule_2_not_validated_hypothesis(
            ms_oracle.levels[level].oracle, ms_oracle.levels[level].link, ms_oracle.levels[level].actual_char,
            ms_oracle.levels[level].actual_char_ind)
    else:
        test_2 = 1
    if not segmentation_rules_mso.RULE_1 and not segmentation_rules_mso.RULE_2:
        test_1 = 0
        test_2 = 0
    if segmentation_rules_mso.RULE_4:
        test_4, potential_obj = segmentation_rules_mso.rule_4_recomputed_object(
            ms_oracle, matrix, level, ms_oracle.levels[level].actual_char_ind, str_obj, k, ms_oracle.level_max, end_mk)
    else:
        test_4 = 0
    if segmentation_rules_mso.RULE_3 and test_4 == 0:
        test_3 = segmentation_rules_mso.rule_3_existing_object(
            ms_oracle.levels[level].materials.history, ms_oracle.levels[level].concat_obj.labels,
            ms_oracle.levels[level].actual_char, matrix)
    else:
        test_3 = 0
    if segmentation_rules_mso.RULE_5:
        test_5 = segmentation_rules_mso.rule_5_regathering(ms_oracle.levels[level].concat_obj.labels)
    else:
        test_5 = 1

    if test_4:
        str_obj = potential_obj
        input_data = [ord(potential_obj[ms_oracle.levels[level].iterator]) - LETTER_DIFF for i in range(len(potential_obj))]

        ms_oracle.levels[level].iterator = len(ms_oracle.levels[level].concat_obj)
        ms_oracle.levels[level].shift = len(ms_oracle.levels[level].oracle.data) - len(
            ms_oracle.levels[level].concat_obj) - 1
        ms_oracle.levels[level].oracle.add_state(input_data[i])
        ms_oracle.levels[level].actual_char = ms_oracle.levels[level].oracle.data[ms_oracle.levels[level].shift + ms_oracle.levels[level].iterator + 1]
        ms_oracle.levels[level].data_length = len(ms_oracle.levels[level].formal_diagram.material_lines[0])
        ms_oracle.levels[level].formal_diagram.update(
            ms_oracle.levels[level].actual_char, ms_oracle.levels[level].actual_char_ind, ms_oracle, level)
        ms_oracle.levels[level].formal_diagram_graph.update(ms_oracle, level)

    return test_1, test_2, test_3, test_4, test_5, str_obj, i, k, input_data


def structure(ms_oracle, level, end_mk):
    """ Function for the structuring operation and therfore the update of the structures at this level and next level"""
    # Labelling upper level string and updating the different structures
    new_char = similarity_rules.char_next_level_similarity(ms_oracle, level)
    if len(ms_oracle.levels) > level + 1:
        node = max(ms_oracle.levels[level][1]) + 1
    else:
        node = 1
    for ind in range(len(ms_oracle.levels[level].concat_obj.labels)):
        ms_oracle.levels[level].link.append(node)

    # send to the next f_oracle the node corresponding to concat_obj
    fun_segmentation(ms_oracle, new_char, level + 1, end_mk)
    return 0


# ================================= MAIN COGNITIVE ALGORITHM AT SYMBOLIC SCALE =========================================
def fun_segmentation(ms_oracle, str_obj, level=0, end_mk=0):
    """This function browses the string char and structure it at the upper level according to the rules that are applied
    by the extern user."""
    # end of the recursive loop
    # str_obj = ms_oracle.levels[level].char
    print("level", level)
    print("ms_oracle.level_max", ms_oracle.level_max)
    if level > ms_oracle.level_max and end_mk == 1:
        return 0

    #  Initialisation of the structures
    if level > ms_oracle.level_max:
        if verbose == 1:
            print("[INFO] CREATION OF NEW FO : LEVEL " + str(level) + "...")
        print(str_obj)
        class_mso.MSOLevel(ms_oracle, str_obj)
        ms_oracle.levels[level].init_oracle('f')
        matrix = ms_oracle.matrix

        if level == 0 and processing == 'symbols':
            vec = [1]
            ms_oracle.matrix = [chr(LETTER_DIFF + ord(str_obj[0])), [vec]]
        elif level > 0:
            matrix = ms_oracle.levels[level - 1].materials.sim_matrix

    else:
        if level > 0:
            matrix = ms_oracle.levels[level - 1].materials.sim_matrix
        else:
            # TODO: @jcalandra 10/09/2021 - matrix storage at level 0
            #  réfléchir au stockage de la matrice de niveau 0
            matrix = ms_oracle.matrix

    # Every new character is analysed.
    input_data = [ord(str_obj[ind_input]) - LETTER_DIFF for ind_input in range(len(str_obj))]
    level_wait = -1
    global wait
    ms_oracle.levels[level].shift = len(ms_oracle.levels[level].oracle.data) - 1
    k = ms_oracle.levels[level].shift
    i = 0
    if verbose == 1:
        print("[INFO] Process in level " + str(level) + "...")
    while i < len(str_obj):
        ms_oracle.levels[level].oracle.add_state(input_data[i])
        actual_char = ms_oracle.levels[level].oracle.data[k + i + 1]  # i_th parsed character
        actual_char_ind = k + i + 1

        if level == 0 and processing == 'symbols' and \
                actual_char > max([ord(ms_oracle.matrix[0][ind]) for ind in range(len(ms_oracle.matrix[0]))]):
            vec = [0 for ind_vec in range(len(ms_oracle.matrix[0]))]
            vec.append(1)
            ms_oracle.matrix[0] += chr(actual_char + LETTER_DIFF)
            ms_oracle.matrix[1].append(vec)
            for ind_mat in range(len(ms_oracle.matrix[1]) - 1):
                ms_oracle.matrix[1][ind_mat].append(ms_oracle.matrix[1][len(ms_oracle.matrix[1]) - 1][ind_mat])

        # formal diagram is updated with the new char
        if actual_char_ind == 1:
            ms_oracle.levels[level].formal_diagram.init(ms_oracle, level)
        else:
            ms_oracle.levels[level].formal_diagram.update(actual_char, actual_char_ind, ms_oracle, level)

        ms_oracle.levels[level].formal_diagram_graph.update(ms_oracle, level)

        # First is the parametrisation of the rules according to the external settings.
        test_1, test_2, test_3, test_4, test_5, i, k, str_obj, input_data = rules_parametrization(
                matrix, ms_oracle, level, i, k, str_obj, input_data, end_mk)

        if level > 0 and end_mk == 1 and i < len(str_obj) - 1:
            end_mk = 0
            wait = 1
            level_wait = level

        # If the tests are positives, there is structuration.
        if ((test_1 and test_2) or (test_2 and test_3) or test_4) and test_5 and (end_mk == 0):
            # or (end_mk == 1 and len(ms_oracle.levels[level].concat_obj_obj.labels) != 0):
            structure(ms_oracle, level, end_mk)
            if verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            ms_oracle.levels[level].concat_obj_obj.labels = ''
        ms_oracle.levels[level].concat_obj_obj.labels = \
            ms_oracle.levels[level].concat_obj_obj.labels + chr(actual_char + LETTER_DIFF)

        # Automatically structuring if this is the End Of String
        if (level == 0 and i == len(str_obj) - 1) or (wait == 1 and level == level_wait and i == len(str_obj) - 1):
            end_mk = 1
            wait = 0
            level_wait = -1
        if end_mk == 1:
            structure(ms_oracle, level, end_mk)
            if verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            ms_oracle.levels[level].concat_obj_obj.labels = ''
        i += 1
        if verbose == 1:
            print("state number ", i, " in level ", level)

    return 1
