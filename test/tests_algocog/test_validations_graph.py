import time
import algo_cog_vmo as ac
import interface as ui
import matplotlib.pyplot as plt
# --- HOP LENGTH ---
HOP_LENGTH_MIN = 512  # 512
HOP_LENGTH_MAX = 4096  # 4096
HOP_LENGTH_STEP = 2  # 2
# --- TETA ---
TETA_MIN = 0.965  # 0.85
TETA_MAX = 0.985  # 0.95
TETA_STEP = 0.001  # 0.01
# --- TEMPO ---
TEMPO_MIN = 50  # 50
TEMPO_MAX = 1000  # 1000
TEMPO_STEP = 50  # has to be a multiple of 50
# --- INIT ---
INIT = 0  # 0
INIT_STEP = 25  # 10
# --- OCTAVE ---
OCTAVE_MIN = 1  # 0
OCTAVE_MAX = 5  # 6
OCTAVE_STEP = 1  # 1
# --- NOTE ---
NOTE_MIN = 5  # 5
NOTE_MAX = 5  # 5
NOTE_STEP = 1  # 1

F_MIN = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#',  'A', 'A#', 'B']
GAP = 3  # difference between the first note and the lowest note on the analysed audio
F_MIN_LEN = len(F_MIN)
PRECISION = 4
NB_MFCC = 48*PRECISION
PATH_RESULTS = "../results/Geisslerlied/validations_vmo/auto/"


def graph_distance(name, teta, hop_length, path_result, label_x, tab_x, tab_distances):
    graph_type = path_result.split('/')[-3]
    plt.figure(figsize=(24, 16))
    plt.plot(tab_x, tab_distances)
    plt.xlabel(label_x)
    plt.ylabel('Edition distance/total number of frames')
    path_name = graph_type + "_teta" + str(teta) + "_hoplength" + str(hop_length) + ".png"
    plt.title(name + " : Edition distance per total number of frames according to the " + label_x + " at teta " +
              str(teta) + " and hop length " + str(hop_length))
    # plt.show()
    plt.savefig(path_result + path_name)
    plt.close()


def graphes_distance(name, path_result, graph_type, tabs_distances):
    plt.figure(figsize=(24, 16))
    file = open(PATH_RESULTS + "data.txt", "a")
    file.write(graph_type + "\n")
    for i in range(len(tabs_distances)):
        file.write(str(tabs_distances[i]) + "\n")
        plt.plot(tabs_distances[i][3], tabs_distances[i][0],
                 label=str(tabs_distances[i][1]) + "-" + str(tabs_distances[i][2]))
    file.close()
    plt.xlabel(graph_type)
    plt.ylabel('Edition distance/total number of frames')
    path_name = "graph/" + graph_type + ".png"
    plt.title(name + " : Edition distance per total number of frames according to the " + graph_type)
    plt.legend()
    # plt.show()
    plt.savefig(path_result + path_name)
    plt.close()


def test_init_cond_graph(name, teta, hop_length, tabs_distances):
    path = '../data/songs/' + name + '.wav'
    path_result1 = PATH_RESULTS + "cond_init/diagcog/"
    path_result2 = PATH_RESULTS + "cond_init/graph/"
    label_x = "beginning frame"
    init = INIT
    tab_distance = []
    tab_x = []
    tab_x2 = []
    factor = HOP_LENGTH_MAX/hop_length
    while init < hop_length:
        print("[INFO] INIT = " + str(init) + "\nHOP_LENGTH = " + str(hop_length) + ", TETA = " + str(teta))
        matrix, data_length, data_size, distance, t = ac.algo_cog(path, hop_length, NB_MFCC, teta, init)
        ui.graph_algo_cogn(name, path_result1, matrix, NB_MFCC, data_length, teta, hop_length, init)
        file = open(PATH_RESULTS + "time.txt", "a")
        file.write(str(t) + " " + str(teta) + " " + str(hop_length) + " " + str(init) + "\n")
        file.close()
        tab_distance.append(distance)
        tab_x.append(init)
        tab_x2.append(init * factor)
        init = init + INIT_STEP
    tabs_distances.append([tab_distance, teta, hop_length, tab_x2])
    graph_distance(name, teta, hop_length, path_result2, label_x, tab_x, tab_distance)


def test_tempo_graph(name, teta, hop_length, tabs_distances):
    actual_tempo = TEMPO_MIN
    actual_name = name + str(actual_tempo)
    path = '../data/songs/' + actual_name + '.wav'
    path_result1 = PATH_RESULTS + "tempo/diagcog/"
    path_result2 = PATH_RESULTS + "tempo/graph/"
    tab_distance = []
    tab_x = []
    label_x = "tempo"
    while actual_tempo < TEMPO_MAX + TEMPO_STEP:
        print("[INFO] TEMPO = " + str(actual_tempo) + "\nHOP_LENGTH = " + str(hop_length) + ", TETA = " + str(teta))
        matrix, data_length, data_size, distance, t = ac.algo_cog(path, hop_length, NB_MFCC, teta, INIT)
        ui.graph_algo_cogn(actual_name, path_result1, matrix, NB_MFCC, data_length, teta, hop_length, INIT)
        file = open(PATH_RESULTS + "time.txt", "a")
        file.write(str(t) + " " + str(teta) + " " + str(hop_length) + " " + str(actual_tempo) + "\n")
        file.close()
        tab_distance.append(distance)
        tab_x.append(actual_tempo)
        actual_tempo = actual_tempo + TEMPO_STEP
        actual_name = name + str(actual_tempo)
        path = '../data/songs/' + actual_name + '.wav'
    tabs_distances.append([tab_distance, teta, hop_length, tab_x])
    graph_distance(name, teta, hop_length, path_result2, label_x, tab_x, tab_distance)


def test_transpose_graph(name, teta, hop_length, tabs_distances):
    actual_transpo_octave = OCTAVE_MIN
    actual_transpo_note = NOTE_MIN
    str_note = F_MIN[actual_transpo_note - GAP]
    it = 0
    while abs(GAP - it) != 0:
        if F_MIN[F_MIN_LEN - GAP + it] == str_note:
            str_octave = str(actual_transpo_octave)
            break
        it = it + 1
    else:
        str_octave = str(actual_transpo_octave + 1)
    str_fmin = str_note + str_octave
    note = '0' + str(actual_transpo_note)
    actual_name = name + str(actual_transpo_octave) + '-' + note
    path = '../data/songs/' + actual_name + '.wav'
    path_result1 = PATH_RESULTS + "transpo/diagcog/"
    path_result2 = PATH_RESULTS + "transpo/graph/"
    label_x = "label of transposition"
    tab_distance = []
    tab_x = []
    while actual_transpo_octave < OCTAVE_MAX or \
            (actual_transpo_octave < OCTAVE_MAX + 1 and actual_transpo_note < NOTE_MAX):
        if actual_transpo_note < 12:
            print("[INFO] TRANSPOSITION = " + str(actual_transpo_octave) + "-" + note +
                  "\nHOP_LENGTH = " + str(hop_length) + ", TETA = " + str(teta))
            matrix, data_length, data_size, distance, t = ac.algo_cog(path, hop_length, NB_MFCC, teta, INIT, str_fmin)
            ui.graph_algo_cogn(actual_name, path_result1, matrix, NB_MFCC, data_length, teta, hop_length, INIT)
            file = open(PATH_RESULTS + "time.txt", "a")
            file.write(str(t) + " " + str(teta) + " " + str(hop_length) + " "
                       + str(actual_transpo_octave) + "-" + str(actual_transpo_note) + "\n")
            file.close()
            tab_distance.append(distance)
            tab_x.append(str(actual_transpo_octave) + "-" + str(actual_transpo_note))

        if actual_transpo_note >= 11:
            actual_transpo_note = 00
            actual_transpo_octave = actual_transpo_octave + OCTAVE_STEP
        else:
            actual_transpo_note = actual_transpo_note + NOTE_STEP

        if actual_transpo_note < 10:
            note = '0' + str(actual_transpo_note)
        else:
            note = str(actual_transpo_note)

        str_note = F_MIN[actual_transpo_note - GAP]

        it = 0
        while abs(GAP - it) != 0:
            if F_MIN[F_MIN_LEN - GAP + it] == str_note:
                str_octave = str(actual_transpo_octave)
                break
            it = it + 1
        else:
            str_octave = str(actual_transpo_octave + 1)
        if str_fmin == 'F4':  # limit
            str_fmin = 'F4'
        else:
            str_fmin = str_note + str_octave
        actual_name = name + str(actual_transpo_octave) + '-' + note
        path = '../data/songs/' + actual_name + '.wav'
    tabs_distances.append([tab_distance, teta, hop_length, tab_x])
    graph_distance(name, teta, hop_length, path_result2, label_x, tab_x, tab_distance)


def test_auto(name):
    hop_length = HOP_LENGTH_MIN
    tabs_distances_cond_init = []
    tabs_distances_tempo = []
    tabs_distances_transpo = []
    while hop_length < HOP_LENGTH_MAX * HOP_LENGTH_STEP:
        teta = TETA_MIN
        while teta < TETA_MAX + TETA_STEP:
            # test_init_cond_graph(name, teta, hop_length, tabs_distances_cond_init)
            # test_tempo_graph(name, teta, hop_length, tabs_distances_tempo)
            test_transpose_graph(name, teta, hop_length, tabs_distances_transpo)
            teta = teta + TETA_STEP
        hop_length = hop_length * HOP_LENGTH_STEP
    # graphes_distance(name, PATH_RESULTS, 'cond init', tabs_distances_cond_init)
    # graphes_distance(name, PATH_RESULTS, 'tempo', tabs_distances_tempo)
    graphes_distance(name, PATH_RESULTS, 'transpo', tabs_distances_transpo)


def main():
    name = "Geisslerlied/Geisslerlied"
    start_time = time.time()
    test_auto(name)
    print("Temps d execution : %s secondes ---" % (time.time() - start_time))


main()
