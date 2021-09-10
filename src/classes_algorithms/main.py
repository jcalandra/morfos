import time
import matplotlib.pyplot as plt

import parameters as prm
import class_mso
import class_signal
import interface as ui
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
    """ Main function of the cognitive algorithm."""
    path = PATH_OBJ + NAME + FORMAT
    start_time_full = time.time()
    mso = class_mso.MSO(NAME, path)
    mso.get_audio(path)
    class_signal.algo_cog(path, mso)
    print("Temps d execution de l'algorithme entier : %s secondes ---" % (time.time() - start_time_full))

    # printing the results in the shell
    for i in range(len(mso.levels)):
        print("new_fd_" + str(i) + ": ", mso.levels[i].formal_diagram)
        print("link_" + str(i) + ": ", mso.levels[i].link)
        print("history next : ", mso.levels[i].materials.history)
        print("matrix_next : ",  mso.levels[i].materials.sim_matrix)
    plt.pause(3000)


main()
