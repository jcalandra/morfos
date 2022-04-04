from algo_segmentation_mso import *
import matplotlib.pyplot as plt
import plot
import objects_storage as obj_s

# This is the main loop starting the algorithm from a string
# Remarque: ce fichier est probablement voué à être supprimé


# =========================================== MAIN FUNCTION FROM STRING ================================================
def main(char_ex):
    """ Main loop for the cognitive algorithm using the MSO and a string describing the audio."""
    # initialisation of the structures
    data_length = len(char_ex)
    level_max = -1
    tab_f_oracle = []
    oracles = [level_max, tab_f_oracle]
    fun_segmentation(oracles, char_ex, data_length)
    new_fd = []

    # printing the results in the shell
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

    if prm.COMPUTE_COSTS:
        print("lambda = ", prm.lambda_0)
        print("gamma = ", prm.gamma)
        print("alpha = ", prm.alpha)
        print("delta = ", prm.delta)
        print("beta = ", prm.beta)

        print("lambda_tab = ", prm.lambda_tab)
        print("lambda_time = ", prm.lambda_time)
        print("gamma_tab = ", prm.gamma_tab)
        print("gamma_time = ", prm.gamma_time)
        print("alpha_tab = ", prm.alpha_tab)
        print("alpha_time = ", prm.alpha_time)
        print("delta_tab = ", prm.delta_tab)
        print("delta_time = ", prm.delta_time)
        print("beta_tab = ", prm.beta_tab)
        print("beta_time = ", prm.beta_time)

        plt.figure(figsize=(32, 20))
        plt.title("lambda")
        plt.xlabel("time")
        plt.ylabel("cost")
        plt.plot(prm.lambda_time, prm.lambda_tab)
        plt.figure(figsize=(32, 20))
        plt.title("gamma")
        plt.xlabel("time")
        plt.ylabel("cost")
        plt.plot(prm.gamma_time, prm.gamma_tab)
        plt.figure(figsize=(32, 20))
        plt.title("alpha")
        plt.xlabel("time")
        plt.ylabel("cost")
        plt.plot(prm.alpha_time, prm.alpha_tab)
        plt.figure(figsize=(32, 20))
        plt.title("delta")
        plt.xlabel("time")
        plt.ylabel("cost")
        plt.plot(prm.delta_time, prm.delta_tab)
        plt.figure(figsize=(32, 20))
        plt.title("beta")
        plt.xlabel("time")
        plt.ylabel("cost")
        plt.plot(prm.beta_time, prm.beta_tab)

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
    main(Geisslerlied)

example()

