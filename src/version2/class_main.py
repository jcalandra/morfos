import time
import matplotlib.pyplot as plt
import module_parameters.parameters as prm
import module_visualization.class_fd2DVisu as fd2D
import os
import class_mso
import class_cog_algo
import precomputer as pc
import costs
import hypothesis
import json
import others.object_storage as obj_s
import shutil
from pathlib import Path


# This is the main loop for the whole cognitive algorithm

NAME = prm.NAME
FORMAT = prm.FORMAT

PATH_SOUND = prm.PATH_SOUND
PATH_RESULT = prm.PATH_RESULT

HOP_LENGTH = prm.HOP_LENGTH
NB_VALUES = prm.NB_VALUES
TETA = prm.TETA
INIT = prm.INIT


# ======================================= COGNITIVE ALGORITHM MAIN FUNCTION ============================================
def main_print(mso):
    # printing the results in the shell
    for level in range(len(mso.levels)):
        mso.levels[level].print()
    plt.pause(3000)


def main():
    """ Main loop for the cognitive algorithm starting from a string describing the audio."""
    # initialisation of the structures
    prm.mk_rule3 = 0
    start_time = time.time()
    path = PATH_SOUND + NAME + FORMAT
    pre_data = None
    costs.init_cost()

    if FORMAT == ".txt":
        pre_data = NAME
    elif format == ".npy":
        pass
    else:
        pre_data = path
    print("format pre", FORMAT)
    data = pc.precompute_data(pre_data)
    obj_tab = pc.compute_data(data)

    mso = class_mso.MSO(NAME)
    obj_s.data_init(data)
    mso.dims = data[3]
    mso.volume = data[2]
    mso.get_data(pre_data, obj_tab)
    class_cog_algo.fun_segmentation(mso, obj_tab)

    end_time = time.time()
    print("Temps d execution de l'algorithme : %s secondes ---" % (end_time - start_time))

    if prm.TO_SAVE_FINAL:
        print("path result :", prm.PATH_RESULT)
        if not os.path.exists(prm.PATH_RESULT):
            os.makedirs(prm.PATH_RESULT)
        fd2D.final_save_one4all(mso)
        fd2D.final_save_all4one(mso)
        shutil.copy2(str(Path(__file__).resolve().parents[1]) +
                     '/version2/parameters.json', prm.PATH_RESULT+'/parameters.json')

    if prm.COMPUTE_HYPOTHESIS:
        hypothesis.print_phases()

    if prm.COMPUTE_COSTS:
        if not os.path.exists(prm.PATH_RESULT):
            os.makedirs(prm.PATH_RESULT)
        costs.normalise_cost()
        costs.print_cost()
        costs.save_cost()
        costs.cost_general_diagram_all_levels()

    if prm.SAVE_MATERIALS:
        with open(prm.PATH_RESULT + '/materials.json', 'w') as myFile:
            json.dump(obj_s.objects, myFile)



    plt.pause(3000)


# Here is a simple example with the analysis of a single string 'abacabacdeabfgabachijklmhinopqabacrsrsttu'
def example():
    """ Exemple with the string char_ex"""
    Geisslerlied = 'abcdadbbdbcddcdeaafaedaedcd'
    Debussy3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 1, 2, 3, 4, 9, 20, 21,
                20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 28, 29, 32, 33, 34, 35, 1, 2, 3, 4, 5, 6, 36, 37, 9, 38,
                39, 9, 39, 40, 1, 39, 40, 41, 42]
    Debussy4 = ''
    for i in range(len(Debussy3)):
        Debussy4 += chr(Debussy3[i] + 96)
    Debussy2 = 'abcdefabcghijklabcfmnopqrstustvwabcdxfyzfzaz'
    Debussy = 'abccddeefabccggghijjjklabccfmnopqrstuusttvwwwabccddxxfyzfzzazfzzfz'
    Mozart = 'abacabacdeabfgabachijklmhinopqabacrsrsttu',".txt"


main()

