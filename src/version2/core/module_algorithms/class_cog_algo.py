from module_parameters.parameters import LETTER_DIFF, verbose, checkpoint
import module_parameters.parameters as prm
import class_similarity_computation
import tests_administrator as ta
import class_mso
import class_concatObj
import costs
import sys
import hypothesis
import time_manager as tm
import numpy as np

# In this file is defined the main loop for the algorithm at symbolic scale
# structring test function according to rules (rules_parametrization) and similarity test function


# TODO: modifier les objets: un objet doit être une structure qui contient
#  - un label
#  - un ensemble de fonctions et les paramètres associés

# ================================= MAIN COGNITIVE ALGORITHM AT SYMBOLIC SCALE =========================================

def gestion_level(ms_oracle,level):
    if level > ms_oracle.level_max and ms_oracle.end_mk == 1:
        return 0
    #  Initialisation of the structures
    if level > ms_oracle.level_max:
        tm.time_add_level()
        if prm.COMPUTE_HYPOTHESIS:
            hypothesis.hypobit_add_level()
        if prm.COMPUTE_COSTS:
            costs.costs_add_level()
        if verbose == 1:
            print("[INFO] CREATION OF NEW FO : LEVEL " + str(level) + "...")
        class_mso.MSOLevel(ms_oracle)
        ms_oracle.levels[level].init_oracle('a', dim=ms_oracle.dims)

        if level == 0:
            ms_oracle.matrix.sim_matrix.init(chr(LETTER_DIFF), [1])
    return 1

def add_obj_level_up(ms_oracle, level):
    new_obj_tab = class_similarity_computation.char_next_level_similarity(ms_oracle, level)
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
    if level == 0:
        tm.init_time()
        if prm.COMPUTE_HYPOTHESIS:
            print("init hypo")
            hypothesis.hypobit_init()
        if prm.COMPUTE_COSTS:
            print("init cost")
            costs.init_cost()
        gestion_level(ms_oracle, level)
        #print(ms_oracle.volume)
        ms_oracle.levels[level].volume = ms_oracle.volume
    rules = ta.Rules()
    ms_oracle.levels[level].objects = objects
    if verbose == 1:
        print("[INFO] Process in level " + str(level) + "...")

    # Every new character is analysed.
    ms_oracle.levels[level].shift = len(ms_oracle.levels[level].oracle.data) - 1
    ms_oracle.levels[level].iterator = 0
    while ms_oracle.levels[level].iterator < len(objects) :
        iterator = ms_oracle.levels[level].iterator
        if level == 0 and ms_oracle.end_mk == 0:
            ms_oracle.levels[level].volume = ms_oracle.volume
            ms_oracle.levels[level].update_oracle(ms_oracle, level)
        ms_oracle.levels[level].actual_object = objects[iterator]
        #print("level", level, "actual obj", ms_oracle.levels[level].actual_object.label)

        if level == 0:
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
        # formal diagram is updated with the new char

        if ms_oracle.levels[level].actual_char_ind == 1:
            ms_oracle.levels[level].formal_diagram.init(ms_oracle, level)
        else:
            ms_oracle.levels[level].formal_diagram.update(ms_oracle, level)

        ms_oracle.levels[level].formal_diagram_graph.update(ms_oracle, level)

        objects = ms_oracle.levels[level].objects
        iterator = ms_oracle.levels[level].iterator

        if (level == 0 and ms_oracle.levels[level].actual_char_ind == len(objects)):
            ms_oracle.end_mk = 1

        if prm.COMPUTE_COSTS:
            costs.compute_cost(ms_oracle, level)

        # If the tests are positives, there is structuration.
        if ((ms_oracle.levels[level].iterator > 0 and level ==0 or level > 0) and ms_oracle.end_mk == 0 and ta.segmentation_test(ms_oracle, level, rules)):
            if ms_oracle.out:
                return 1
            # print("segmentation 1")
            if len(ms_oracle.levels) > level + 1:
                ms_oracle.levels[level + 1].shift = len(ms_oracle.levels[level + 1].oracle.data) - 1
                ms_oracle.levels[level + 1].iterator = 0
            if prm.COMPUTE_HYPOTHESIS:
                bit_seg = 1
                hypothesis.bit_seg_add(level, bit_seg)
                if len(prm.bit_class[level]) > 1:
                    hypothesis.compute_phases(level, ms_oracle.end_mk)
            structure(ms_oracle, level)
            if verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            ms_oracle.levels[level].concat_obj = class_concatObj.ConcatObj()
            ms_oracle.levels[level].concat_obj.init(ms_oracle.levels[level].actual_object)
        else:
            if ms_oracle.out:
                return 1
            # print("no segmentation")
            if level == 0 and ms_oracle.levels[level].iterator == len(objects):
                break
            if prm.COMPUTE_HYPOTHESIS:
                bit_seg = 0
                hypothesis.bit_seg_add(level, bit_seg)
                if len(prm.bit_class[level]) > 1:
                    hypothesis.compute_phases(level, ms_oracle.end_mk)
                if ms_oracle.end_mk == 1 and level == ms_oracle.level_max:
                    bit_seg = 1
                    hypothesis.bit_seg_add(level, bit_seg)
                    if len(prm.bit_class[level]) > 1:
                        hypothesis.compute_phases(level, ms_oracle.end_mk)
            if ms_oracle.levels[level].concat_obj.size == 0:
                ms_oracle.levels[level].concat_obj.init(ms_oracle.levels[level].actual_object)
            else:
                ms_oracle.levels[level].concat_obj.update(ms_oracle.levels[level].actual_object)

        # Automatically structuring if this is the End Of String
        if ms_oracle.end_mk == 1 and ms_oracle.level_max > level:
            if ms_oracle.out:
                return 1
            # print("segmentation 2")
            if ms_oracle.level_max > level:
                ms_oracle.levels[level + 1].iterator -= 1
            if prm.COMPUTE_HYPOTHESIS:
                bit_seg = 1
                hypothesis.bit_seg_add(level, bit_seg)
                if len(prm.bit_class[level]) > 1:
                    hypothesis.compute_phases(level, ms_oracle.end_mk)
            structure(ms_oracle, level)
            ms_oracle.levels[level].concat_obj = class_concatObj.ConcatObj()
            ms_oracle.levels[level].concat_obj.init(ms_oracle.levels[level].actual_object)
            if verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
        ms_oracle.levels[level].iterator += 1
        if verbose == 1:
            print("state number ", iterator, " in level ", level)

    return 1
