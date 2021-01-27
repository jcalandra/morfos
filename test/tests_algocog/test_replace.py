import time
import numpy as np
import midi as md
import signal_ac as sig
import discovery_front as df
import interface as ui
import matplotlib.pyplot as plt

BACKGROUND = (255, 255, 255)

# TODO : modifier de telle sorte à ce que ce soit fonctionnel pour des matrices numpy
# TODO : finir l'implémentation


def compute_replace(matrix_midi, matrix_audio):
    """ replace the frames in audio matrix according to the MIDI matrix."""

    df_midi = df.discovery_front_computing(matrix_midi, BACKGROUND)
    df_audio = df.discovery_front_computing(matrix_audio, BACKGROUND)

    print("[INFO] Modifying audio matrix according to MIDI matrix...")
    copy_matrix_audio = matrix_audio.copy()
    copy_df_audio = df_audio

    err = 0
    nb_mat_audio = len(df_audio)
    nb_mat_midi = len(df_midi)
    print("len df midi =" + str(nb_mat_midi))
    print("len df audio =" + str(nb_mat_audio))

    error_line = np.ones((1, len(copy_matrix_audio[0]), 3), np.uint8)
    for i in range(len(copy_matrix_audio[0])):
        error_line[0][i] = BACKGROUND

    i = i_min = i_max = 0
    case = ""
    m_ok = 0
    while i < len(df_midi):
        # considérer le cas où le dernier mat est manquant dans l'audio : sinon on a une erreur ici
        if df_midi[i][0] < df_audio[i][0]:
            # on a pas assez de matériaux audio
            i_min = df_midi[i][0]
            i_max = df_audio[i][0]
            case = "inf"

        if df_midi[i][0] > df_audio[i][0]:
            # on a trop de matériaux audio
            i_min = df_audio[i][0]
            i_max = df_midi[i][0]
            case = "sup"

        for j in range(i_min, i_max):
            m_ok = nb_mat_audio
            # On supprime les frames là où elles ne sont pas censées être dans le diagramme audio
            # Il faut du coup la remettre là où elle est censée être sur cette colonne
            # On incrémente l'erreur de 1 pour chaque audio qui n'est pas censé être à cette place
            for k in range(df_midi[i][1] + 1):
                if (matrix_midi[k][j][0] != BACKGROUND[0] or matrix_midi[k][j][1] != BACKGROUND[1] or
                        matrix_midi[k][j][2] != BACKGROUND[2]) and (matrix_audio[k][j][0] == BACKGROUND[0] and
                                                                    matrix_audio[k][j][1] == BACKGROUND[1] and
                                                                    matrix_audio[k][j][2] == BACKGROUND[2]):
                    if j == i_min and case == "inf":
                        new_line = np.ones((1, len(copy_matrix_audio[0]), 3), np.uint8)
                        for i in range(len(copy_matrix_audio[0])):
                            new_line[0][i] = BACKGROUND
                        copy_matrix_audio = np.concatenate((copy_matrix_audio[:i], new_line, copy_matrix_audio[i:]))
                    copy_matrix_audio[k][j] = matrix_midi[k][j]
                    err = err + 1
                    m_ok = k
                if k != m_ok:
                    copy_matrix_audio[k][j] = BACKGROUND
        if case == "inf":
            df_audio.insert(i, df_midi(i))
            for i1 in range(i + 1, len(df_audio)):
                df_audio[i1][1] = df_audio[i1][1] + 1
        elif case == "sup":
            # Peut-être ici que je peux tout simplement enregistrer les indices de colonne ainsi que la valeur car dans
            # tous les cas je dois parcourir l'intégralité de la file
            for i1 in range(len(copy_matrix_audio[0])):
                if matrix_audio[i][i1][0] != BACKGROUND[0] or matrix_audio[i][i1][1] != BACKGROUND[1] or \
                        matrix_audio[i][i1][2] != BACKGROUND[2]:
                    error_line[0][i1] = matrix_audio[i][i1]
            matrix_audio = np.delete(matrix_audio, i, axis=0)
            if m_ok < i:
                df_audio.pop(i)
                for i1 in range(i, len(df_audio)):
                    df_audio[i1][1] = df_audio[i1][1] - 1
            elif m_ok > i:
                df_audio.pop(i + 1)
                for i1 in range(i + 1, len(df_audio)):
                    df_audio[i1][1] = df_audio[i1][1] - 1
    return err, matrix_audio, matrix_midi


def print_replace(matrix_audio_mdfy, matrix_midi, name, data_length, hop_length, teta):
    """ compute and print the difference between the modified audio matrix and the MIDI matrix"""
    mat_diff = []
    diff = 0
    nb_mat_audio = len(matrix_audio_mdfy)
    nb_mat_midi = len(matrix_midi)
    length_audio = len(matrix_audio_mdfy[0])
    length_midi = len(matrix_midi[0])

    if nb_mat_audio != nb_mat_midi:
        print("The two matricies don't have the same number of materials")
    if length_audio != length_midi:
        print("The two matrices don't have the same length")

    for i in range(nb_mat_audio):
        line_diff = []
        for j in range(length_audio):
            el_diff = abs(matrix_audio_mdfy[i][j] - matrix_midi[i][j])
            line_diff.append(el_diff)
            diff = diff + el_diff
        mat_diff.append(line_diff)
    diff = diff/(nb_mat_audio*length_audio)
    plt.figure(figsize=(15, 5))
    plt.title("Matrice différentielle " + name + " hoplength" + str(hop_length) + " teta" + str(teta))
    plt.gray()
    plt.xlabel("temps (mémoire forme)")
    plt.ylabel("matériau (mémoire matériau)")
    plt.imshow(mat_diff, extent=[0, data_length, len(mat_diff), 0])
    plt.show()
    plt.close()
    return diff


def test_replace(name, hop_length, nb_mfcc, teta, init, tempo):
    print("[INFO] MODIFICATION PROCESSING")
    path_wav = '../data/songs/' + name + '.wav'
    path_midi = '../data/midi/' + name + '.mid'

    print("[INFO] Comparing the audio and midi matrices of " + str(name) + "...")

    start_time = time.time()
    matrix_audio, data_length, data_size, distance = sig.algo_cog(path_wav, hop_length, nb_mfcc, teta, init)
    print("[INFO] Execution time audio : %s secondes ---" % (time.time() - start_time))
    ui.graph_algo_cogn(name + "-audio", "",  matrix_audio, nb_mfcc, data_length, teta, hop_length, init)

    start_time = time.time()
    matrix_midi = md.interface(path_midi, hop_length, tempo)
    print("[INFO] Execution time midi : %s secondes ---" % (time.time() - start_time))

    err, mat_audio_mdfy = compute_replace(matrix_midi, matrix_audio)
    diff = print_replace(mat_audio_mdfy, matrix_midi, name, data_length, hop_length, teta)
    return err, diff


def main():
    mat1 = [[0, 1, 1, 1], [0, 1, 0, 0], [1, 1, 1, 1]]
    mat2 = [[1, 1, 1, 1], [0, 0, 0, 1], [1, 1, 1, 1]]
    diff = print_replace(mat1, mat2, "name", 3, 1, 2)
    print(diff)


main()
