import time
import algo_cog as ac
import algo_cog_rep as acr
import algo_cog_vmo as acvmo
import interface as ui
import parameters as prm

NAME = prm.NAME
FORMAT = prm.FORMAT

PATH_OBJ = prm.PATH_OBJ
PATH_RESULT = prm.PATH_RESULT

HOP_LENGTH = prm.HOP_LENGTH
NB_VALUES = prm.NB_VALUES
TETA = prm.TETA
INIT = prm.INIT

ALGO_VMO = prm.ALGO_VMO
ALGO_REP = prm.ALGO_REP
ALGO_USUAL = prm.ALGO_USUAL


def main():
    path = PATH_OBJ + NAME + FORMAT
    start_time_full = time.time()
    matrix = data_length = None
    if ALGO_VMO:
        matrix, data_length, data_size, distance, t = acvmo.algo_cog(path, HOP_LENGTH, NB_VALUES, TETA, INIT)
    elif ALGO_REP:
        matrix, data_length, data_size, distance, t = acr.algo_cog(path, HOP_LENGTH, NB_VALUES, TETA, INIT)
    elif ALGO_USUAL:
        matrix, data_length, data_size, distance, t = ac.algo_cog(path, HOP_LENGTH, NB_VALUES, TETA, INIT)
    print("Temps d execution de l'algorithme entier : %s secondes ---" % (time.time() - start_time_full))
    ui.graph_algo_cogn(NAME, PATH_RESULT, matrix, NB_VALUES, data_length, TETA, HOP_LENGTH, INIT)


main()
