# ======== PATH IMPORT ========

# Add python_path to perform relative import
# main_mso.py must stay on src

import json
import sys
import os
from pathlib import Path # if you haven't already done so


file = Path(__file__).resolve()
import shutil

project_root = str(file.parents[1])

src_path = project_root
sys.path.append(src_path)

generic_path = src_path + '/version1/generic'
sys.path.append(generic_path)

oracle_path = src_path + '/version1/oracle_version'
sys.path.append(oracle_path)
print("oracle path", oracle_path)

plot_path = project_root + '/version1/lib/vmo-master/vmo'
sys.path.append(plot_path)

misc_path = plot_path + '/version1/VMO/utility'
sys.path.append(misc_path)

misc_path = plot_path + '/version1/VMO/utility'
sys.path.append(misc_path)

# ======== IMPORT ======== 

import time
import matplotlib.pyplot as plt
import data_mso
import version1.parameters as prm
import objects_storage as obj_s
import scipy.io.wavfile as wave
import cost_storage as cs
import phases_storage as hs
from formal_diagram_mso import final_save_one4all, final_save_all4one
import audacity_marker
# import formal_diagram_mso as fd_mso

# This is the main loop for the whole cognitive algorithm

NAME = prm.NAME
FORMAT = prm.FORMAT

PATH_SOUND = prm.PATH_SOUND
PATH_RESULT = prm.PATH_RESULT
PATH = PATH_SOUND + NAME + FORMAT

# ======================================= COGNITIVE ALGORITHM MAIN FUNCTION ============================================
def main(path=PATH, result_path=prm.PATH_RESULT):
    """ Main function of the cognitive algorithm producing a hiérarchy of formal diagrams from signal using MSO."""
    #path = PATH_SOUND + NAME + FORMAT
    start_time_full = time.time()

    level_max = -1
    tab_f_oracle = []
    audio = []
    mso_oracle = [level_max, tab_f_oracle, audio]
    obj_s.objects_init()
    obj_s.first_occ_init()

    data_mso.algo_cog(path, mso_oracle)
    if prm.SHOW_TIME:
        print("Temps d execution de l'algorithme entier : %s secondes ---" % (time.time() - start_time_full))

    data_length = len(mso_oracle[1][0][1])
    new_fd = []

    # printing the results in the shell
    if prm.SHOW_MSO_CONTENT:
        for i in range(len(mso_oracle[1])):
            new_fd.append([tab_f_oracle[i][0].data[j]
                           for j in range(1, len(tab_f_oracle[i][0].data))])
            print("new_fd_" + str(i) + ": ", new_fd[i])
            print("link_" + str(i) + ": ", mso_oracle[1][i][1])
            print("history next : ", mso_oracle[1][i][2])
            print("matrix_next : ", mso_oracle[1][i][6])

            for j in range(len(obj_s.objects[i])):
                print("elmt id:",obj_s.objects[i][j]["id"],
                      "links:", obj_s.objects[i][j]["links"],
                      "coordinates: x=", obj_s.objects[i][j]["coordinates"]["x"],
                      " y=",obj_s.objects[i][j]["coordinates"]["y"],
                      " z=", obj_s.objects[i][j]["coordinates"]["z"],
                      "mat num:", obj_s.objects[i][j]["mat_num"],
                      "level:", obj_s.objects[i][j]["level"],
                      "len sound:", len(obj_s.objects[i][j]["sound"]))

                if prm.SYNTHESIS:
                    name = PATH_RESULT + "/synthesis/" +\
                           path.split('/')[-1][:-4]+ "_level" + str(i) + "_obj" + str(j) + "_synthesis.wav"
                    wave.write(name, prm.SR, obj_s.objects[i][j]["sound"])

            if prm.PLOT_ORACLE:
                im = plot.start_draw(tab_f_oracle[i][0], size=(900 * 4, 400 * 4))
                im.show()

    if prm.TO_SAVE_FINAL:
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        final_save_one4all(mso_oracle, data_length, result_path)
        final_save_all4one(mso_oracle, data_length, result_path)
        shutil.copy2(src_path +
                     '/version1/parameters.json', prm.PATH_RESULT+'/parameters.txt')
        print('file saved as ' + prm.PATH_RESULT+ '/parameters.txt')

    audacity_marker.produce_file(obj_s.objects)

    if prm.COMPUTE_HYPOTHESIS:
        hs.phases_print()
        hs.phases_cost_diagram_perphase()
        hs.phases_cost_diagram_perlevel()
        secondary_phases_tab = hs.sphases_computing(prm.hypo)
        hs.sphases_cost_diagram(secondary_phases_tab)
        sphase = hs.cost_per_sphase(secondary_phases_tab, prm.cost_total_tab)
        hs.sphases_cost_diagram_perlevel(sphase)

    if prm.COMPUTE_COSTS and prm.SHOW_COMPUTE_COSTS:
        # cs.cost_oracle_print()
        cs.cost_general_print()
        # cs.cost_oracle_diagram_all_levels()
        cs.cost_general_diagram_all_levels()
        # cs.cost_general_diagram_allinone()

    if prm.TO_SHOW_PYP or prm.SHOW_COMPUTE_COSTS:
        plt.pause(3000)

    if prm.SAVE_MATERIALS:
        with open(prm.PATH_RESULT + '/materials.json', 'w') as myFile:
            json.dump(obj_s.objects, myFile)
        print('file saved as ' + prm.PATH_RESULT+ '/materials.json')

        file = open(prm.PATH_RESULT + "/structure.txt", "w")
        for i in range(len(mso_oracle[1])):
            file.write("level" + str(i) + "\n")
            new_fd.append([tab_f_oracle[i][0].data[j]
                           for j in range(1, len(tab_f_oracle[i][0].data))])
            file.write("new_fd: " + str(new_fd[i])+ "\n")
            file.write("link: " + str(mso_oracle[1][i][1])+ "\n")
            file.write("history table: " + str(mso_oracle[1][i][2])+ "\n")
            file.write("material similarity matrix: "+ str(mso_oracle[1][i][6])+ "\n\n")
        file.close()
        print('file saved as ' + prm.PATH_RESULT+ '/structure.txt')


main()