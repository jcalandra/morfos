import time
import signal_ac as sig
import signal_rep as sig_r
import data_mso as sig_mso
import interface as ui
import parameters as prm

NAME = prm.NAME
FORMAT = prm.FORMAT

PATH_SOUND = prm.PATH_SOUND
PATH_RESULT = prm.PATH_RESULT

HOP_LENGTH = prm.HOP_LENGTH
NB_VALUES = prm.NB_VALUES
TETA = prm.TETA
INIT = prm.INIT

ALGO_VMO = prm.ALGO_VMO
ALGO_REP = prm.ALGO_REP
ALGO_USUAL = prm.ALGO_USUAL

# This file contain the main loop to get the diagram only at the first level which is signal scale
# Remarque: ce fichier est probablement voué à être supprimé


# ==================================== MAIN FUNCTION FOR FIRST LEVEL DIAGRAM ===========================================
def main():
    """Main loop to get the formal diagram at level 0 (signal scale)."""
    path = PATH_SOUND + NAME + FORMAT
    start_time_full = time.time()
    level_max = -1
    tab_f_oracle = []
    mso_oracle = [level_max, tab_f_oracle]
    matrix = data_length = None
    if ALGO_VMO:
        matrix, data_length, data_size, distance, t = sig_mso.algo_cog(path, mso_oracle)
    elif ALGO_REP:
        matrix, data_length, data_size, distance, t = sig_r.algo_cog(path, HOP_LENGTH, NB_VALUES, TETA, INIT)
    elif ALGO_USUAL:
        matrix, data_length, data_size, distance, t = sig.algo_cog(path, HOP_LENGTH, NB_VALUES, TETA, INIT)
    print("Temps d execution de l'algorithme entier : %s secondes ---" % (time.time() - start_time_full))
    ui.graph_algo_cogn(NAME, PATH_RESULT, matrix, NB_VALUES, data_length, TETA, HOP_LENGTH, INIT)


main()
