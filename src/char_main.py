from algo_segmentation_mso import *
import matplotlib.pyplot as plt

# This is the main loop starting the algorithm from a string
# Remarque: ce fichier est probablement voué à être supprimé
# TODO: maj pour que ce soit à nouveau fonctionnel


# =========================================== MAIN FUNCTION FROM STRING ================================================
def main(char_ex):
    """ Main loop for the cognitive algorithm starting from a string describing the audio."""
    # initialisation of the structures
    data_length = len(char_ex)
    level_max = -1
    tab_f_oracle = []
    oracles = [level_max, tab_f_oracle]
    fun_segmentation(oracles, char_ex, data_length)
    new_fd = []

    # printing the results in the shell
    for i in range(len(oracles[1])):
        new_fd.append([chr(tab_f_oracle[i][0].data[j] + letter_diff) for j in range(1, len(tab_f_oracle[i][0].data))])
        print("new_fd_" + str(i) + ": ", new_fd[i])
        print("link_" + str(i) + ": ", oracles[1][i][1])
        print("history next : ", oracles[1][i][2])
    plt.pause(300)


# Here is a simple example with the analysis of a single string 'abacabacdeabfgabachijklmhinopqabacrsrsttu'
def example():
    """ Exemple with the string char_ex"""
    char_ex2 = 'abacabacdeabfgabachijklmabacdeabhinopqabacrsrsttu'
    char_ex = 'abacabacdeabfgabachijklmhinopqabacrsrsttu'
    # main(char_ex2)
    main(char_ex)


example()
