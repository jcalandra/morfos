from module_parameters.parameters import LETTER_DIFF, processing, verbose, checkpoint
import class_similarity_rules
import tests_administrator as ta
import class_mso
import class_concatObj
import sys

# In this file is defined the main loop for the algorithm at symbolic scale
# structring test function according to rules (rules_parametrization) and similarity test function
wait = 0


# TODO: modifier les objets: un objet doit être une structure qui contient
#  - un label
#  - un ensemble de fonctions et les paramètres associés

# ================================= MAIN COGNITIVE ALGORITHM AT SYMBOLIC SCALE =========================================

def gestion_level(ms_oracle,level):
    if level > ms_oracle.level_max and ms_oracle.end_mk == 1:
        return 0

    #  Initialisation of the structures
    if level > ms_oracle.level_max:
        if verbose == 1:
            print("[INFO] CREATION OF NEW FO : LEVEL " + str(level) + "...")
        class_mso.MSOLevel(ms_oracle)
        ms_oracle.levels[level].init_oracle('a')

        if level == 0 and processing == 'symbols':
            ms_oracle.matrix.init(chr(LETTER_DIFF), [1])
    return 1

def add_obj_level_up(ms_oracle, level):
    new_obj_tab = class_similarity_rules.char_next_level_similarity(ms_oracle, level)
    return new_obj_tab


def structure(ms_oracle, level):
    """ Function for the structuring operation and therfore the update of the structures at this level and next level"""
    # Labelling upper level string and updating the different structures
    sim = gestion_level(ms_oracle,level+1)
    if sim:
        new_obj_tab = add_obj_level_up(ms_oracle,level+1)

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
    if level == 0 and processing == 'symbols':
        gestion_level(ms_oracle, level)
    rules = ta.Rules()
    level_wait = -1
    global wait
    ms_oracle.levels[level].objects = objects
    if verbose == 1:
        print("[INFO] Process in level " + str(level) + "...")

    # Every new character is analysed.
    ms_oracle.levels[level].shift = len(ms_oracle.levels[level].oracle.data) - 1
    ms_oracle.levels[level].iterator = 0
    while ms_oracle.levels[level].iterator < len(objects):
        iterator = ms_oracle.levels[level].iterator
        if level == 0:
            ms_oracle.levels[level].update_oracle(ms_oracle, level)
        ms_oracle.levels[level].actual_object = objects[iterator]

        if level == 0 and processing == 'symbols':
            # CHECKPOINT #
            # Si le format fournit en entrée du logiciel est une chaîne de caractères.
            # Vous trouvez ici l'information concernant l'avancement du calcul de l'algorithme (approximatif, ne prend pas
            # en compte certaines spécificités de comportement de l'algorithme possible aux niveaux supérieurs).
            # Envoi beaucoup d'information (autant que d'éléments au niveau 0), on peut donc choisir de filtrer seulement
            # certaines valeurs
            cp = (ms_oracle.levels[level].shift + ms_oracle.levels[level].iterator)/(ms_oracle.levels[level].shift + len(objects))*100
            if checkpoint == 1:
                print("CHECKPOINT: ", cp)
                sys.stdout.flush()
            # END CHECKPOINT #

            ms_oracle.levels[level].oracle.objects.append(ms_oracle.levels[level].actual_object)
            if ord(ms_oracle.levels[level].actual_object.label)> \
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
        bool = ta.segmentation_test(ms_oracle, level, rules)
        objects = ms_oracle.levels[level].objects
        iterator = ms_oracle.levels[level].iterator
        if level > 0 and ms_oracle.end_mk == 1 and iterator < len(objects) - 1:
            ms_oracle.end_mk = 0
            wait = 1
            level_wait = level

        if (level == 0 and iterator == ms_oracle.levels[level].actual_char_ind) or \
                (wait == 1 and level == level_wait and iterator == len(objects) - 1):
            ms_oracle.end_mk = 1
            wait = 0
            level_wait = -1

        # If the tests are positives, there is structuration.
        if (bool and ms_oracle.end_mk == 0) or (level == 0 and ms_oracle.end_mk == 1):
            if len(ms_oracle.levels) > level + 1:
                ms_oracle.levels[level + 1].shift = len(ms_oracle.levels[level + 1].oracle.data) - 1
                ms_oracle.levels[level + 1].iterator = 0
            structure(ms_oracle, level)
            if verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            ms_oracle.levels[level].concat_obj = class_concatObj.ConcatObj()
            ms_oracle.levels[level].concat_obj.init(ms_oracle.levels[level].actual_object)
        else:
            if ms_oracle.levels[level].concat_obj.size == 0:
                ms_oracle.levels[level].concat_obj.init(ms_oracle.levels[level].actual_object)
            else:
                ms_oracle.levels[level].concat_obj.update(ms_oracle.levels[level].actual_object)

        # Automatically structuring if this is the End Of String
        if level > 0 and ms_oracle.end_mk == 1 and ms_oracle.level_max >= level:
            if ms_oracle.level_max > level:
                ms_oracle.levels[level + 1].iterator -= 1
            structure(ms_oracle, level)
            ms_oracle.levels[level].concat_obj = class_concatObj.ConcatObj()
            ms_oracle.levels[level].concat_obj.init(ms_oracle.levels[level].actual_object)

            if verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
        ms_oracle.levels[level].iterator += 1
        if verbose == 1:
            print("state number ", iterator, " in level ", level)

    return 1
