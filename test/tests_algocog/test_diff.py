import time
import numpy as np
import matplotlib.pyplot as plt
import midi as md
import algo_cog as ac
import interface as ui
import discovery_front as dfront
import parameters as prm


HOP_LENGTH = prm.HOP_LENGTH
NB_VALUES = prm.NB_VALUES
TETA = prm.TETA
TEMPO = 120
INIT = prm.INIT

BACKGROUND = (255, 255, 255)


def del_column(mtx_err, mtx, i, fd):
    """ Function to delete both columns of matrix and matrix_error. Might be deleted."""
    size = 1
    # size = 0
    # while (fd + size) < len(mtx_err[i]) and mtx_err[i][fd + size] == 0:
    #     size = size + 1
    mtx_err = np.delete(mtx_err, np.s_[fd:fd + size], axis=1)
    mtx = np.delete(mtx, np.s_[fd:fd + size], axis=1)
    return mtx_err, mtx


def clear_matrix(mtx_audio, mtx_midi, data_size, data_length, hop_length):
    """ Function that clear matrices by deleting the lines in mtx_audio that contains frames considered as
    non-representative of a material and delete the columns of the corresponding non representative frames in mtx_audio
    and mtx_midi. Not that useful now because we created in algo_cog an algorithm that replace the non-representative
    frames. """
    print("[INFO] Clearing Matrices...")
    # clear matrix
    mtx_audio_clean = mtx_audio.copy()
    mtx_midi_clean = mtx_midi.copy()

    # il faut changer ça car on a ajouté du silence. nb_hop = len(mtx_audio[0])
    nb_hop = int(data_size / hop_length) + 1
    to_remove = []
    nb_hop_sec = data_size / (data_length * hop_length)  # nb_hop_sec = nb_hop/frame_rate ?
    audio_length_min = nb_hop_sec / 10  # nb hop corresponding to 1/20sec
    window = int(nb_hop_sec / 4)  # nb hop corresponding to 1/4sec

    # Detect the lines where there is only fragments of size < audio_length_min and register their indice in to_remove
    for i in range(1, len(mtx_audio_clean)):
        note_length = 0
        for j in range(nb_hop):
            value = 0
            if mtx_audio_clean[i][j][0] == BACKGROUND[0] and mtx_audio_clean[i][j][1] == BACKGROUND[1] and \
                    mtx_audio_clean[i][j][2] == BACKGROUND[2]:
                value = 1
            note_length = note_length + (1 - value)
            if (j % window) == 0:
                if note_length <= audio_length_min:
                    note_length = 0
                else:
                    break
        if note_length < audio_length_min:
            to_remove.append(i)

    # For each lines that are to remove, find the first element that appears, its size, and remove the column
    # associated with that element.
    print("len diag audio =" + str(len(mtx_audio_clean)))
    print("len diag midi = " + str(len(mtx_midi_clean)))
    ns_lines = len(to_remove)
    print("number of non significant lines =", ns_lines)
    print("to remove :")
    print(to_remove)
    fd = 0
    for i in to_remove:
        print(i)
        while fd < len(mtx_audio_clean[i]) and mtx_audio_clean[i][fd][0] == BACKGROUND[0] and \
                mtx_audio_clean[i][fd][1] == BACKGROUND[1] and mtx_audio_clean[i][fd][2] == BACKGROUND[2]:
            fd = fd + 1
        if fd < len(mtx_audio_clean[i]):
            mtx_audio_clean, mtx_midi_clean = del_column(mtx_audio_clean, mtx_midi_clean, i, fd)

        # Remove the lines of materials that are considered as non significants
        mtx_audio_clean = np.delete(mtx_audio_clean, i, axis=0)
        for j in range(len(to_remove)):
            to_remove[j] = to_remove[j] - 1
    return mtx_audio_clean, mtx_midi_clean, ns_lines


def df_comparison(diag_midi, diag_audio, data_size, data_length, hop_length):
    """ The function clear_matrix is applied, then the discovery front are computed. From that """
    copy_diag_audio, copy_diag_midi, ns_lines = clear_matrix(diag_audio, diag_midi, data_size, data_length, hop_length)

    df_midi = dfront.discovery_front_computing(copy_diag_midi, BACKGROUND)
    df_audio = dfront.discovery_front_computing(copy_diag_audio, BACKGROUND)

    print("[INFO] Comparing matrices...")
    copy_diag_err = []
    copy_diag = []
    df_err = df_midi
    df = df_audio

    sup_lines = 0
    inf_lines = 0
    print("len fd midi =" + str(len(df_midi)))
    print("len fd audio =" + str(len(df_audio)))

    i = 0
    while i < len(df_err):
        if i < len(df_audio) and i < len(df_midi) and df_midi[i][0] != df_audio[i][0]:
            if df_midi[i][0] < df_audio[i][0]:
                copy_diag_err = copy_diag_midi
                copy_diag = copy_diag_audio
                df_err = df_midi
                df = df_audio
                inf_lines = inf_lines + 1

            if df_midi[i][0] > df_audio[i][0]:
                copy_diag_err = copy_diag_audio
                copy_diag = copy_diag_midi
                df_err = df_audio
                df = df_midi
                sup_lines = sup_lines + 1

            # ON SUPPRIME LES COLONNES DE TROP, LES COLONNES CORRESPONDANTES DE L'AUTRE MATRICE
            # ET ON DECALE LES INDICES
            copy_diag_err = np.delete(copy_diag_err, df_err[i][0],
                                      axis=1)  # supprime la colonne de trop dans copy_audio
            # del copy_diag_err[j1][df_err[i][0]:df_err[i + 1][0]]
            copy_diag = np.delete(copy_diag, df_err[i][0], axis=1)

            err = 1
            # err = df_err[i + 1][0] - df_err[i][0]
            for k in range(i, len(df)):
                df[k][0] = df[k][0] - err
            for k in range(i + 1, len(df_err)):
                df_err[k][0] = df_err[k][0] - err

            copy_diag_err = np.delete(copy_diag_err, df_err[i][1], axis=0)  # supprime la ligne de trop dans copy_audio
            df_err.pop(i)  # supprime le matériau du front de découverte de audio
            k = i
            while k < len(df_err):
                df_err[k][1] = df_err[k][1] - 1
                k = k + 1
            print("discovery front midi : ", df_midi)
            print("discovery front audio : ", df_audio)
        else:
            i = i + 1

    while len(df_audio) > len(df_midi):
        n = len(df_audio) - 1
        i = df_audio[n][0]
        copy_diag_audio, copy_diag_midi = del_column(copy_diag_audio, copy_diag_midi, n, i)

        copy_diag_audio = np.delete(copy_diag_audio, df_audio[n][1], axis=0)
        df_audio.pop(n)
        sup_lines = sup_lines + 1

    while len(df_midi) > len(df_audio):
        n = len(df_midi) - 1
        i = df_midi[n][0]
        copy_diag_midi, copy_diag_audio = del_column(copy_diag_midi, copy_diag_audio, n, i)

        copy_diag_midi = np.delete(copy_diag_midi, df_midi[n][1], axis=0)
        df_midi.pop(n)
        inf_lines = inf_lines + 1

    print("[RESULT] inf lines =" + str(inf_lines) + ", sup lines = " + str(sup_lines))
    return copy_diag_midi, copy_diag_audio, ns_lines, inf_lines, sup_lines


def compute_diff(mtx_midi, mtx_audio):
    print("[INFO] Computing the difference between the two matrices...")
    if len(mtx_audio[0]) != len(mtx_midi[0]):
        print("[WARNING] The two matrices don't have the same length of time !")
        return -1
    if len(mtx_audio) != len(mtx_midi):
        print("[WARNING] The two matrices don't have the same number of materials !")
        blank_line = np.ones((1, len(mtx_audio[0]), 3), np.uint8)
        for i in range(len(mtx_audio[0])):
            blank_line[0][i] = BACKGROUND
        while len(mtx_audio) < len(mtx_midi):
            mtx_audio = np.concatenate((mtx_audio, blank_line))
        while len(mtx_midi) < len(mtx_audio):
            mtx_midi = np.concatenate((mtx_midi, blank_line))
    print("[RESULT] matrix_audio size (materiau,temps) = (" + str(len(mtx_audio)) + ", " + str(len(mtx_audio[0])) + ")")
    print("[RESULT] matrix_midi size (materiau, temps) = (" + str(len(mtx_midi)) + ", " + str(len(mtx_midi[0])) + ")")

    nb_mat = len(mtx_audio)
    nb_hop = len(mtx_audio[0])
    diff = 0
    mat_diff = []
    for i in range(nb_mat):
        line = []
        for j in range(nb_hop):
            value_audio = value_midi = 0
            if mtx_audio[i][j][0] == BACKGROUND[0] and mtx_audio[i][j][1] == BACKGROUND[1] and \
                    mtx_audio[i][j][2] == BACKGROUND[2]:
                value_audio = 1
            if mtx_midi[i][j][0] == BACKGROUND[0] and mtx_midi[i][j][1] == BACKGROUND[1] and \
                    mtx_midi[i][j][2] == BACKGROUND[2]:
                value_midi = 1
            el_diff = abs(value_audio - value_midi)
            line.append(el_diff)
            diff = diff + el_diff
        mat_diff.append(line)
    diff = diff / (nb_mat * nb_hop)
    print("[RESULT] The difference between the matrices is : ", diff)
    return diff, mat_diff


def print_diff(mat_diff, name, data_length, hop_length, teta):
    plt.figure(figsize=(15, 5))
    plt.title("Matrice différentielle " + name + " hoplength" + str(hop_length) + " teta" + str(teta))
    plt.gray()
    plt.xlabel("temps (mémoire forme)")
    plt.ylabel("matériau (mémoire matériau)")
    plt.imshow(mat_diff, extent=[0, data_length, len(mat_diff), 0])
    path_results = "../results/" + name + "/test_diff/"
    plt.savefig(path_results + "mtxdiff_" + name + "_hoplength" + str(hop_length) + "_teta" + str(teta) + ".png")
    plt.show()
    plt.close()


def test_diff(name, hop_length, nb_values, teta, tempo, init):
    print("[INFO] DIFFERENTIAL PROCESSING")
    path_wav = '../data/songs/Geisslerlied/' + name + '.wav'
    path_midi = '../data/midi/' + name + '.mid'

    print("[INFO] Comparing the audio and midi matrices of " + str(name) + "...")

    start_time = time.time()
    matrix_audio, data_length, data_size, distance, t = ac.algo_cog(path_wav, hop_length, nb_values, teta, init)
    print("[INFO] Execution time audio : %s secondes ---" % (time.time() - start_time))
    ui.graph_algo_cogn(name + "-audio", "", matrix_audio, nb_values, data_length, teta, hop_length, init)

    start_time = time.time()
    matrix_midi = md.interface(path_midi, tempo)
    print("[INFO] Execution time midi : %s secondes ---" % (time.time() - start_time))

    copy_matrix_midi, copy_matrix_audio, ns_lines, inf_lines, sup_lines = df_comparison(matrix_midi, matrix_audio,
                                                                                        data_size, data_length,
                                                                                        hop_length)

    ui.graph_algo_cogn(name + "-midi-clean", "", copy_matrix_midi, nb_values, data_length, teta, hop_length, init)
    ui.graph_algo_cogn(name + "-audio-clean", "", copy_matrix_audio, nb_values, data_length, teta, hop_length, init)

    diff, mat_diff = compute_diff(copy_matrix_midi, copy_matrix_audio)
    print_diff(mat_diff, name, data_length, hop_length, teta)
    nb_mat = len(matrix_midi)
    return ns_lines, inf_lines, sup_lines, diff, nb_mat


def main():
    name = "Geisslerlied"
    test_diff(name, HOP_LENGTH, NB_VALUES, TETA, TEMPO, INIT)


main()
