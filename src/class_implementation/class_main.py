import time
import matplotlib.pyplot as plt

import parameters as prm
import class_mso
import class_signal
import class_cog_algo

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
def main():
    """ Main function of the cognitive algorithm."""
    path = PATH_SOUND + NAME + FORMAT
    start_time_full = time.time()
    mso = class_mso.MSO(NAME)
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


def main_char(char_ex):
    """ Main loop for the cognitive algorithm starting from a string describing the audio."""
    # initialisation of the structures
    nb_hop = len(char_ex)
    mso = class_mso.MSO(NAME)
    mso.get_symbol(char_ex, nb_hop)
    class_cog_algo.fun_segmentation(mso, [], char_ex)

    # printing the results in the shell
    for i in range(len(mso.levels)):
        print("new_fd_" + str(i) + ": ", mso.levels[i].formal_diagram)
        print("link_" + str(i) + ": ", mso.levels[i].link)
        print("history next : ", mso.levels[i].materials.history)
        print("matrix_next : ",  mso.levels[i].materials.sim_matrix)
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
    print(Debussy4)
    Debussy2 = 'abcdefabcghijklabcfmnopqrstustvwabcdxfyzfzaz'
    Debussy = 'abccddeefabccggghijjjklabccfmnopqrstuusttvwwwabccddxxfyzfzzazfzzfz'
    Mozart = 'abacabacdeabfgabachijklmhinopqabacrsrsttu'
    main_char(Mozart)


example()

