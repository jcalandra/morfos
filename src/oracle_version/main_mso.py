import time
import matplotlib.pyplot as plt
import signal_mso as sig_mso
import parameters as prm

NAME = prm.NAME
FORMAT = prm.FORMAT

PATH_OBJ = prm.PATH_OBJ
PATH_RESULT = prm.PATH_RESULT

HOP_LENGTH = prm.HOP_LENGTH
NB_VALUES = prm.NB_VALUES
TETA = prm.TETA
INIT = prm.INIT


def main():
    path = PATH_OBJ + NAME + FORMAT
    start_time_full = time.time()

    level_max = -1
    tab_f_oracle = []
    mso_oracle = [level_max, tab_f_oracle]

    sig_mso.algo_cog(path, mso_oracle, HOP_LENGTH, NB_VALUES, TETA, INIT)
    print("Temps d execution de l'algorithme entier : %s secondes ---" % (time.time() - start_time_full))

    new_fd = []

    # printing the results in the shell
    for i in range(len(mso_oracle[1])):
        new_fd.append([chr(tab_f_oracle[i][0].data[j] + sig_mso.fd_mso.letter_diff)
                       for j in range(1, len(tab_f_oracle[i][0].data))])
        print("new_fd_" + str(i) + ": ", new_fd[i])
        print("link_" + str(i) + ": ", mso_oracle[1][i][1])
        print("history next : ", mso_oracle[1][i][2])
    plt.pause(1200)


main()
