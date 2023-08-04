from module_parameters.parameters import LETTER_DIFF, processing, verbose
import class_similarity_rules
import tests_administrator as ta
import class_mso
from object_model import class_object

# In this file is defined the main loop for the algorithm at symbolic scale
# structring test function according to rules (rules_parametrization) and similarity test function
wait = 0


# TODO: modifier les objets: un objet doit être une structure qui contient
#  - un label
#  - un ensemble de fonctions et les paramètres associés


# ============================================ SEGMENTATION FUNCTION ===================================================

def obj_to_label(objects):
    str_obj = ""
    for obj in objects:
        str_obj += obj.label
    return str_obj

def obj_to_labelTab(objects):
    str_obj = obj_to_label(objects)
    label_data = [ord(str_obj[ind_input]) - LETTER_DIFF for ind_input in range(len(str_obj))]
    return label_data



def structure(ms_oracle, level):
    """ Function for the structuring operation and therfore the update of the structures at this level and next level"""
    # Labelling upper level string and updating the different structures
    new_obj_tab = class_similarity_rules.char_next_level_similarity(ms_oracle, level)
    if len(ms_oracle.levels) > level + 1:
        node = max(ms_oracle.levels[level].link) + 1
    else:
        node = 1
    for ind in range(ms_oracle.levels[level].concat_obj.size):
        ms_oracle.levels[level].link.append(node)
    label = ""
    for obj in new_obj_tab:
        label += obj.label
    # send to the next f_oracle the node corresponding to concat_obj
    fun_segmentation(ms_oracle, new_obj_tab, level + 1)
    return 0


# ================================= MAIN COGNITIVE ALGORITHM AT SYMBOLIC SCALE =========================================
def fun_segmentation(ms_oracle, objects, level=0):
    """This function browses the string char and structure it at the upper level according to the rules that are applied
    by the extern user."""
    # end of the recursive loop
    rules = ta.Rules()
    if level > ms_oracle.level_max and ms_oracle.end_mk == 1:
        return 0

    #  Initialisation of the structures
    if level > ms_oracle.level_max:
        if verbose == 1:
            print("[INFO] CREATION OF NEW FO : LEVEL " + str(level) + "...")
        class_mso.MSOLevel(ms_oracle)
        ms_oracle.levels[level].init_oracle('f')

        if level == 0 and processing == 'symbols':
            ms_oracle.matrix.init(chr(LETTER_DIFF + 1), [1])

    # Every new character is analysed.
    label_data = obj_to_labelTab(objects)
    level_wait = -1
    global wait
    ms_oracle.levels[level].objects = objects
    ms_oracle.levels[level].shift = len(ms_oracle.levels[level].oracle.data) - 1
    ms_oracle.levels[level].iterator = 0
    if verbose == 1:
        print("[INFO] Process in level " + str(level) + "...")
    while ms_oracle.levels[level].iterator < len(objects):

        i = ms_oracle.levels[level].iterator
        ms_oracle.levels[level].update_oracle(label_data[i])
        ms_oracle.levels[level].actual_object = objects[i]

        print("ord actual obj", ord(ms_oracle.levels[level].actual_object.label))
        print("mat", max([ord(ms_oracle.matrix.labels[ind]) for ind in range(len(ms_oracle.matrix.labels))]))
        if level == 0 and processing == 'symbols' and \
                ord(ms_oracle.levels[level].actual_object.label)> \
                max([ord(ms_oracle.matrix.labels[ind]) for ind in range(len(ms_oracle.matrix.labels))]):
            print("oui")
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
        # test_1, test_2, test_3, test_4, test_5= ta.rules_parametrization(ms_oracle, level)
        #test_1, test_2, test_3, test_4, test_5 = ta.segmentation_str(ms_oracle, level, rules)
        bool = ta.segmentation_test(ms_oracle, level, rules)
        objects = ms_oracle.levels[level].objects
        label_data = obj_to_labelTab(objects)
        i = ms_oracle.levels[level].iterator
        if level > 0 and ms_oracle.end_mk == 1 and i < len(objects) - 1:
            ms_oracle.end_mk = 0
            wait = 1
            level_wait = level

        # If the tests are positives, there is structuration.
        if bool and (ms_oracle.end_mk == 0):
        #if ((test_1 and test_4) or (test_2 and test_4) or test_3) and test_5 and (ms_oracle.end_mk == 0):
            # or (ms_oracle.end_mk == 1 and len(ms_oracle.levels[level].concat_obj_obj.labels) != 0):
            structure(ms_oracle, level)
            if verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            ms_oracle.levels[level].concat_obj = class_object.ConcatObj()
            ms_oracle.levels[level].concat_obj.init(ms_oracle.levels[level].actual_object)
        else:
            if ms_oracle.levels[level].concat_obj.size == 0:
                ms_oracle.levels[level].concat_obj.init(ms_oracle.levels[level].actual_object)
            else:
                ms_oracle.levels[level].concat_obj.update(ms_oracle.levels[level].actual_object)

        # Automatically structuring if this is the End Of String
        if (level == 0 and i == len(objects) - 1) or (wait == 1 and level == level_wait and i == len(objects) - 1):
            ms_oracle.end_mk = 1
            wait = 0
            level_wait = -1
        if ms_oracle.end_mk == 1:
            structure(ms_oracle, level)
            if verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            ms_oracle.levels[level].concat_obj = class_object.ConcatObj()
        ms_oracle.levels[level].iterator += 1
        if verbose == 1:
            print("state number ", i, " in level ", level)

    return 1
