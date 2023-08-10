import time
import matplotlib.pyplot as plt

import module_parameters.parameters as prm
import class_mso
import class_signal
import class_cog_algo
import class_object

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
    for i in range(len(mso.levels)):
        print("new_fd_" + str(i) + ": ", mso.levels[i].formal_diagram)
        print("link_" + str(i) + ": ", mso.levels[i].link)
        print("history next : ", mso.levels[i].materials.history)
        print("matrix_next : ",  mso.levels[i].materials.sim_matrix)
    plt.pause(3000)


def main():
    """ Main loop for the cognitive algorithm starting from a string describing the audio."""
    # initialisation of the structures
    start_time = time.time()
    path = PATH_SOUND + NAME + FORMAT
    print(FORMAT)
    if FORMAT == ".txt":
        nb_hop = len(NAME)
        obj_tab = []
        for i in range(nb_hop):
            new_rep = class_object.ObjRep()
            new_rep.init([], NAME[i], class_object.Descriptors())
            new_signal = []
            new_descriptors = class_object.Descriptors()
            #new_descriptors.init([["a"],["b"]],[["a"],["b"]])
            new_descriptors.init([[[1]],[[2,2],[2,2]]],[[[1]],[[2,2],[2,2]]])


            new_obj = class_object.Object()
            new_obj.update(new_rep.label, new_descriptors, new_signal, new_rep)
            obj_tab.append(new_obj)

        mso = class_mso.MSO(NAME)
        mso.get_symbol(NAME, nb_hop)
        class_cog_algo.fun_segmentation(mso, obj_tab)

    elif format == ".npy":
        pass
    else:
        mso = class_mso.MSO(NAME)
        mso.get_audio(path)
        class_signal.algo_cog(path, mso)

    end_time = time.time()
    print("Temps d execution de l'algorithme : %s secondes ---" % (end_time - start_time))
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

