# ======== PATH IMPORT ========

# Add python_path to perform relative import
# class_main.py must stay on src/version2
import paths
from pathlib import Path
# ======== IMPORT ===========

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
import somax_marker



# This is the main loop for the whole cognitive algorithm
# TODO: supprimer le niveau 0

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


def main(name=NAME, format=FORMAT, path_sound=PATH_SOUND, path_result=PATH_RESULT):
    # initialisation of the structures
    prm.mk_rule3 = 0
    start_time = time.time()
    path = path_sound + name + format
    pre_data = None
    costs.init_cost()

    if format == ".txt":
        pre_data = name
    elif format == ".npy":
        pass
    else:
        pre_data = path

    data = pc.precompute_data(pre_data)

    obj_tab = pc.compute_data(data)

    mso = class_mso.MSO(name)
    obj_s.data_init(data)
    mso.dims = data[3]
    mso.volume = data[2]
    mso.get_data(pre_data, obj_tab)
    class_cog_algo.fun_segmentation(mso, obj_tab)

    end_time = time.time()
    print("Temps d execution de l'algorithme : %s secondes ---" % (end_time - start_time))


    if prm.TO_SAVE_FINAL:
        #print("path result :", path_result)
        if not os.path.exists(path_result):
            os.makedirs(path_result)
        fd2D.final_save_one4all(mso, path_result)
        fd2D.final_save_all4one(mso, path_result)
    if prm.SAVE_PARAMETERS:
        if not os.path.exists(path_result):
            os.makedirs(path_result)
        if format == ".txt":
            shutil.copy2(str(Path(__file__).resolve().parents[1]) +
                         '/version2/parameters.json', path_result + '/parameters.json')
        else:
            shutil.copy2(str(Path(__file__).resolve().parents[1]) +
                        '/version2/parameters.json', path_result + '/parameters.json')
        print("file saved as " + path_result + '/parameters.json')

    if prm.COMPUTE_HYPOTHESIS:
        hypothesis.print_phases()

    if prm.COMPUTE_COSTS:
        if not os.path.exists(path_result):
            os.makedirs(path_result)
        costs.normalise_cost()
        costs.print_cost()
        costs.save_cost()
        costs.cost_general_diagram_all_levels()

    if prm.SAVE_MATERIALS:
        if not os.path.exists(path_result):
            os.makedirs(path_result)
        with open(path_result + '/materials.json', 'w') as myFile:
            # json.dump(obj_s.objects, myFile)
            json.dump(str(obj_s.objects), myFile)
        print("file saved as " + path_result + '/materials.json')

    somax_marker.produce_file(obj_s.objects, path_result)


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
    Mozart = 'abacabacdeabfgabachijklmhinopqabacrsrsttu'
    loop = 'abababcdefghfghfijabklcdehifgmnop'
    main(name=Mozart)


main()

