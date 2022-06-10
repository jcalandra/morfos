from algo_segmentation_mso import *
import objects_storage as obj_s
import cost_storage as cs
from rwcpop_parser import parser, Path
from formal_diagram_mso import final_save_one4all, final_save_all4one
import matplotlib.pyplot as plt
import plot
import os


# This is the main loop starting the algorithm from a string
# Remarque: ce fichier est probablement voué à être supprimé


# =========================================== MAIN FUNCTION FROM STRING ================================================
def main(char_ex, result_path=prm.PATH_RESULT):
    """ Main loop for the cognitive algorithm using the MSO and a string describing the audio."""
    # initialisation of the structures
    data_length = len(char_ex)
    level_max = -1
    tab_f_oracle = []
    oracles = [level_max, tab_f_oracle]
    fun_segmentation(oracles, char_ex, data_length)
    new_fd = []

    # printing the results in the shell
    if prm.SHOW_MSO_CONTENT:
        for i in range(len(oracles[1])):
            new_fd.append([chr(tab_f_oracle[i][0].data[j]) for j in range(1, len(tab_f_oracle[i][0].data))])
            print("new_fd_" + str(i) + ": ", new_fd[i])
            print("link_" + str(i) + ": ", oracles[1][i][1])
            print("history next : ", oracles[1][i][2])

            for j in range(len(obj_s.objects[i])):
                print("elmt id:",obj_s.objects[i][j]["id"],
                      "links:", obj_s.objects[i][j]["links"],
                      "coordinates: x=", obj_s.objects[i][j]["coordinates"]["x"],
                      " y=",obj_s.objects[i][j]["coordinates"]["y"],
                      " z=", obj_s.objects[i][j]["coordinates"]["z"],
                      "mat num:", obj_s.objects[i][j]["mat_num"],
                      "level:", obj_s.objects[i][j]["level"],
                      "sound:", obj_s.objects[i][j]["sound"])

            if prm.PLOT_ORACLE:
                im = plot.start_draw(tab_f_oracle[i][0], size=(900 * 4, 400 * 4))
                im.show()

    if prm.TO_SAVE_FINAL:
        if not os.path.exists(result_path):
            os.makedirs(result_path)
    final_save_one4all(oracles, data_length, result_path)
    final_save_all4one(oracles, data_length, result_path)

    if prm.COMPUTE_HYPOTHESIS:
        hs.phases_print()
        hs.phases_cost_diagram_perphase()
        hs.phases_cost_diagram_perlevel()
        #secondary_phases_tab = hs.sphases_computing(prm.hypo)
        #hs.sphases_cost_diagram(secondary_phases_tab)

    if prm.COMPUTE_COSTS and prm.SHOW_COMPUTE_COSTS:
        cs.cost_general_print()
        # cs.cost_general_diagram_all_levels_whypothesis()
        # cs.cost_oracle_diagram_all_levels_whypothesis()

    if prm.TO_SHOW_PYP  or prm.SHOW_COMPUTE_COSTS:
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
    Chouvel1 = 'aaabaacbabbaccaadabcabdacdadbadcacaddbbcbbdbccbcdbdcbddcccdcdddaa'
    Chouvel2_post = 'bcdabbccadcbabcaabdbcbdccbbbaadddcddbbdacacdcabacccdbddadbadaaacbc'
    Chouvel2 = 'abcdaabbdcbadabddacabacbbaaaddcccbccaacdbdbcbdadbbbcaccdcadcdddbab'
    main(Mozart)

def rwcpop_tests():
    file = Path(__file__).resolve()
    project_root = str(file.parents[1])
    test_path = project_root + '/data/rwcpop/Pop 71 (grid).csv'
    pop01 = parser(test_path)
    print(pop01)
    main(pop01)

rwcpop_tests()

