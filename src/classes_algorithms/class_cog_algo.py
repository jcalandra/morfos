from parameters import LETTER_DIFF, processing, verbose
import class_segmentation_rules
import class_similarity_rules
import matplotlib.pyplot as plt

import class_mso

# In this file is defined the main loop for the algorithm at symbolic scale
# structring test function according to rules (rules_parametrization) and similarity test function
wait = 0


# TODO: modifier les objets: un objet doit être une structure qui contient
#  - un label
#  - un ensemble de fonctions et les paramètres associés


# ============================================ SEGMENTATION FUNCTION ===================================================
def rules_parametrization(ms_oracle, level, str_obj, input_data, end_mk):
    """ Structuring test function: if one test is validated, there is structuration."""
    potential_obj = None
    if class_segmentation_rules.RULE_1:
        test_1 = class_segmentation_rules.rule_1_similarity(ms_oracle, level)
    else:
        test_1 = 1
    if class_segmentation_rules.RULE_2:
        test_2 = class_segmentation_rules.rule_2_not_validated_hypothesis(ms_oracle, level)
    else:
        test_2 = 1
    if not class_segmentation_rules.RULE_1 and not class_segmentation_rules.RULE_2:
        test_1 = 0
        test_2 = 0
    if class_segmentation_rules.RULE_4:
        test_4, potential_obj = class_segmentation_rules.rule_4_recomputed_object(ms_oracle, level, str_obj, end_mk)
    else:
        test_4 = 0
    if class_segmentation_rules.RULE_3 and test_4 == 0:
        test_3 = class_segmentation_rules.rule_3_existing_object(ms_oracle, level)
    else:
        test_3 = 0
    if class_segmentation_rules.RULE_5:
        test_5 = class_segmentation_rules.rule_5_regathering(ms_oracle, level)
    else:
        test_5 = 1

    if test_4:
        plt.pause(30)
        str_obj = potential_obj
        input_data = [ord(potential_obj[i]) - LETTER_DIFF for i in range(len(potential_obj))]

        ms_oracle.levels[level].iterator = len(ms_oracle.levels[level].concat_obj.concat_labels)
        ms_oracle.levels[level].shift = len(ms_oracle.levels[level].oracle.data) - len(
            ms_oracle.levels[level].concat_obj.concat_labels) - 1
        ms_oracle.levels[level].update_oracle(input_data[ms_oracle.levels[level].iterator])
        ms_oracle.levels[level].actual_char = \
            ms_oracle.levels[level].oracle.data[ms_oracle.levels[level].shift + ms_oracle.levels[level].iterator + 1]
        ms_oracle.levels[level].data_length = len(ms_oracle.levels[level].formal_diagram.material_lines[0])
        ms_oracle.levels[level].formal_diagram.update(ms_oracle, level)
        ms_oracle.levels[level].formal_diagram_graph.update(ms_oracle, level)

    return test_1, test_2, test_3, test_4, test_5, str_obj, input_data


def structure(ms_oracle, level, end_mk):
    """ Function for the structuring operation and therfore the update of the structures at this level and next level"""
    # Labelling upper level string and updating the different structures
    new_char = class_similarity_rules.char_next_level_similarity(ms_oracle, level)
    if len(ms_oracle.levels) > level + 1:
        node = max(ms_oracle.levels[level].link) + 1
    else:
        node = 1
    for ind in range(len(ms_oracle.levels[level].concat_obj.concat_labels)):
        ms_oracle.levels[level].link.append(node)
    # send to the next f_oracle the node corresponding to concat_obj
    fun_segmentation(ms_oracle, new_char, level + 1, end_mk)
    return 0


# ================================= MAIN COGNITIVE ALGORITHM AT SYMBOLIC SCALE =========================================
def fun_segmentation(ms_oracle, str_obj, level=0, end_mk=0):
    """This function browses the string char and structure it at the upper level according to the rules that are applied
    by the extern user."""
    # end of the recursive loop
    if level > ms_oracle.level_max and end_mk == 1:
        return 0

    #  Initialisation of the structures
    if level > ms_oracle.level_max:
        if verbose == 1:
            print("[INFO] CREATION OF NEW FO : LEVEL " + str(level) + "...")
        class_mso.MSOLevel(ms_oracle)
        ms_oracle.levels[level].init_oracle('f')

        if level == 0 and processing == 'symbols':
            vec = [1]
            ms_oracle.matrix.labels = chr(LETTER_DIFF + ord(str_obj[0]))
            ms_oracle.matrix.values = [vec]

    # Every new character is analysed.
    input_data = [ord(str_obj[ind_input]) - LETTER_DIFF for ind_input in range(len(str_obj))]
    level_wait = -1
    global wait
    ms_oracle.levels[level].shift = len(ms_oracle.levels[level].oracle.data) - 1
    ms_oracle.levels[level].iterator = 0
    if verbose == 1:
        print("[INFO] Process in level " + str(level) + "...")
    while ms_oracle.levels[level].iterator < len(str_obj):
        i = ms_oracle.levels[level].iterator
        ms_oracle.levels[level].update_oracle(input_data[i])

        if level == 0 and processing == 'symbols' and \
                ms_oracle.levels[level].actual_char > \
                max([ord(ms_oracle.matrix.labels[ind]) for ind in range(len(ms_oracle.matrix.labels))]):
            vec = [0 for ind_vec in range(len(ms_oracle.matrix.values))]
            vec.append(1)
            ms_oracle.matrix.labels += chr(ms_oracle.levels[level].actual_char + LETTER_DIFF)
            ms_oracle.matrix.values.append(vec)
            for ind_mat in range(len(ms_oracle.matrix.values) - 1):
                ms_oracle.matrix.values[ind_mat].append(
                    ms_oracle.matrix.values[len(ms_oracle.matrix.values) - 1][ind_mat])

        # formal diagram is updated with the new char
        if ms_oracle.levels[level].actual_char_ind == 1:
            ms_oracle.levels[level].formal_diagram.init(ms_oracle, level)
        else:
            ms_oracle.levels[level].formal_diagram.update(ms_oracle, level)

        ms_oracle.levels[level].formal_diagram_graph.update(ms_oracle, level)

        # First is the parametrisation of the rules according to the external settings.
        test_1, test_2, test_3, test_4, test_5, str_obj, input_data = rules_parametrization(
                ms_oracle, level, str_obj, input_data, end_mk)
        i = ms_oracle.levels[level].iterator
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
            ms_oracle.levels[level].concat_obj.concat_labels = ''
        ms_oracle.levels[level].concat_obj.concat_labels = \
            ms_oracle.levels[level].concat_obj.concat_labels + chr(ms_oracle.levels[level].actual_char + LETTER_DIFF)

        # Automatically structuring if this is the End Of String
        if (level == 0 and i == len(str_obj) - 1) or (wait == 1 and level == level_wait and i == len(str_obj) - 1):
            end_mk = 1
            wait = 0
            level_wait = -1
        if end_mk == 1:
            structure(ms_oracle, level, end_mk)
            if verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            ms_oracle.levels[level].concat_obj.labels = ''
        ms_oracle.levels[level].iterator += 1
        if verbose == 1:
            print("state number ", i, " in level ", level)

    return 1
