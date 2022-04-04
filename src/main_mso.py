import time
import plot
import matplotlib.pyplot as plt
import signal_mso as sig_mso
import parameters as prm
import objects_storage as obj_s
import scipy.io.wavfile as wave
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
    print("Temps d execution de l'algorithme entier : %s secondes ---" % (time.time() - start_time_full))

    new_fd = []

    # printing the results in the shell
    for i in range(len(mso_oracle[1])):
        new_fd.append([tab_f_oracle[i][0].data[j]
                       for j in range(1, len(tab_f_oracle[i][0].data))])
        print("new_fd_" + str(i) + ": ", new_fd[i])
        print("link_" + str(i) + ": ", mso_oracle[1][i][1])
        print("history next : ", mso_oracle[1][i][2])
        print("matrix_next : ", mso_oracle[1][i][6])

        if prm.COMPUTE_COSTS:
            plt.figure(figsize=(32, 20))
            plt.title("total cost, level" + str(i))
            plt.xlabel("time")
            plt.ylabel("total cost")
            plt.plot(prm.total_cost_time[i], prm.total_cost_tab[i])

            plt.figure(figsize=(32, 20))
            plt.title("total cost sum, level" + str(i))
            plt.xlabel("time")
            plt.ylabel("total cost sum")
            plt.plot(prm.total_cost_time[i], prm.total_cost_sum[i])

        if prm.verbose:
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
        print("total_cost_tab = ", prm.total_cost_tab)
        print("total_cost_sum = ", prm.total_cost_sum)
        print("total_cost_time = ", prm.total_cost_time)

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

main()
