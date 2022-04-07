# === PATH IMPORT ===

# Add python_path to perform relative import
# main_mso.py must stay on src

import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()

project_root = str(file.parents[1])

src_root = project_root + '/src'
sys.path.append(src_root)

generic_root = src_root + '/generic'
sys.path.append(generic_root)

oracle_root = src_root + '/oracle_version'
sys.path.append(oracle_root)

plot_root = project_root + '/lib/vmo-master/vmo'
sys.path.append(plot_root)

misc_root = plot_root + '/VMO/utility'
sys.path.append(misc_root)

# === IMPORT === 

import time
import plot
import matplotlib.pyplot as plt
import signal_mso as sig_mso
import parameters as prm
import objects_storage as obj_s
import scipy.io.wavfile as wave
import cost_storage as cs
# import formal_diagram_mso as fd_mso

# This is the main loop for the whole cognitive algorithm

NAME = prm.NAME
FORMAT = prm.FORMAT

PATH_OBJ = prm.PATH_OBJ
PATH_RESULT = prm.PATH_RESULT

HOP_LENGTH = prm.HOP_LENGTH
NB_VALUES = prm.NB_VALUES
TETA = prm.TETA
INIT = prm.INIT

# ======================================= COGNITIVE ALGORITHM MAIN FUNCTION ============================================
def main():
    """ Main function of the cognitive algorithm producing a hiérarchy of formal diagrams from signal using MSO."""
    path = PATH_OBJ + NAME + FORMAT
    start_time_full = time.time()

    level_max = -1
    tab_f_oracle = []
    audio = []
    mso_oracle = [level_max, tab_f_oracle, audio]
    obj_s.objects_init()
    obj_s.first_occ_init()

    sig_mso.algo_cog(path, mso_oracle)
    if prm.SHOW_TIME:
        print("Temps d execution de l'algorithme entier : %s secondes ---" % (time.time() - start_time_full))

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
                    name = "cognitive_algorithm_and_its_musical_applications/results/synthesis/" +\
                           path.split('/')[-1][:-4]+ "_level" + str(i) + "_obj" + str(j) + "_synthesis.wav"
                    wave.write(name, prm.SR, obj_s.objects[i][j]["sound"])

            if prm.PLOT_ORACLE:
                im = plot.start_draw(tab_f_oracle[i][0], size=(900 * 4, 400 * 4))
                im.show()

    if prm.COMPUTE_COSTS and prm.SHOW_COMPUTE_COSTS:
        cs.cost_oracle_print()
        cs.cost_general_print()
        cs.cost_oracle_diagram_all_levels()
        cs.cost_general_diagram_all_levels()
        cs.cost_general_diagram_allinone()

    if prm.TO_SHOW_PYP:
        plt.pause(3000)

main()
