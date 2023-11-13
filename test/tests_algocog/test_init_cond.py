import time_manager
import signal_ac as sig
import interface as ui

HOP_LENGTH = 1024
NB_MFCC = 50
TETA = 0.91
INIT = 0
PATH_RESULTS = "../results/validations/auto/"


def test_init_cond(name):
    path = '../data/songs/' + name + '.wav'
    path_result = PATH_RESULTS + "cond_init/" + name + "/"
    init = INIT
    while init < HOP_LENGTH:
        print("[INFO] INIT = ", init)
        matrix, data_length, data_size, distance = sig.algo_cog(path, HOP_LENGTH, NB_MFCC, TETA, init)
        ui.graph_algo_cogn(name, path_result, matrix, NB_MFCC, data_length, TETA, HOP_LENGTH, init)
        init = init + 10


def test_tempo(name):
    actual_tempo = 50
    actual_name = name + str(actual_tempo)
    path = '../data/songs/' + actual_name + '.wav'
    path_result = PATH_RESULTS + "tempo/" + name + "/"
    while actual_tempo < 151:
        print("[INFO] TEMPO = ", actual_tempo)
        matrix, data_length, data_size, distance = sig.algo_cog(path, HOP_LENGTH, NB_MFCC, TETA, INIT)
        ui.graph_algo_cogn(actual_name, path_result, matrix, NB_MFCC, data_length, TETA, HOP_LENGTH, INIT)
        actual_tempo = actual_tempo + 50
        actual_name = name + str(actual_tempo)
        path = '../data/songs/' + actual_name + '.wav'


def test_transpose(name):
    actual_transpo_octave = 1
    actual_transpo_note = 5
    note = '0' + str(actual_transpo_note)
    actual_name = name + str(actual_transpo_octave) + '-' + note
    path = '../data/songs/' + actual_name + '.wav'
    path_result = PATH_RESULTS + "transpo/" + name + "/"
    while actual_transpo_octave < 5 or actual_transpo_note < 5:
        print("[INFO] TRANSPOSITION = " + str(actual_transpo_octave) + "-" + note)
        matrix, data_length, data_size, distance = sig.algo_cog(path, HOP_LENGTH, NB_MFCC, TETA, INIT)
        ui.graph_algo_cogn(actual_name, path_result, matrix, NB_MFCC, data_length, TETA, HOP_LENGTH, INIT)
        if actual_transpo_note == 11:
            actual_transpo_note = 00
            actual_transpo_octave = actual_transpo_octave + 1
        else:
            actual_transpo_note = actual_transpo_note + 1
        if actual_transpo_note < 10:
            note = '0' + str(actual_transpo_note)
        else:
            note = str(actual_transpo_note)
        actual_name = name + str(actual_transpo_octave) + '-' + note
        path = '../data/songs/' + actual_name + '.wav'


def main():
    name = "Geisslerlied"
    file = open("../results/error.txt", "a")
    # file.write("GEISSLERLIED\nTEST INIT_COND\n")
    # file.close()
    start_time = time_manager.time()
    # test_init_cond(name)
    print("Temps d execution : %s secondes ---" % (time_manager.time() - start_time))

    # file.write("\nTEST TEMPO\n")
    # file.close()
    start_time = time_manager.time()
    # test_tempo(name)
    print("Temps d execution : %s secondes ---" % (time_manager.time() - start_time))

    # file.write("\nTEST TRANSPO\n")
    # file.close()
    start_time = time_manager.time()
    test_transpose(name)
    print("Temps d execution : %s secondes ---" % (time_manager.time() - start_time))


main()
