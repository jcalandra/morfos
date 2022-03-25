import time
import plot
import matplotlib.pyplot as plt
import signal_mso as sig_mso
import parameters as prm
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
    prm.objects = []
    prm.first_occ = []

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

        for j in range(len(prm.objects[i])):
            print("elmt id:",prm.objects[i][j]["id"],
                  "links:", prm.objects[i][j]["links"],
                  "coordinates: x=", prm.objects[i][j]["coordinates"]["x"],
                  " y=",prm.objects[i][j]["coordinates"]["y"],
                  " z=", prm.objects[i][j]["coordinates"]["z"],
                  "mat num:", prm.objects[i][j]["mat_num"],
                  "level:", prm.objects[i][j]["level"],
                  "len sound:", len(prm.objects[i][j]["sound"]),
                  "sound:", prm.objects[i][j]["sound"])

            if prm.SYNTHESIS:
                name = "cognitive_algorithm_and_its_musical_applications/results/synthesis/" +\
                       path.split('/')[-1][:-4]+ "_level" + str(i) + "_obj" + str(j) + "_synthesis.wav"
                wave.write(name, prm.SR, prm.objects[i][j]["sound"])

        if prm.PLOT_ORACLE:
            im = plot.start_draw(tab_f_oracle[i][0], size=(900 * 4, 400 * 4))
            im.show()

    if prm.COMPUTE_COSTS:
        print("lambda = ", prm.lambda_0)
        print("gamma = ", prm.gamma)
        print("alpha = ", prm.alpha)
        print("delta = ", prm.delta)
        print("beta = ", prm.beta)

    plt.pause(3000)

main()
