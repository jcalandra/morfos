import matplotlib.pyplot as plt
import cv2
import parameters as prm

# note : pyplot reads pictures in RGB and opencv reads pictures in BGR
MFCC_BIT = prm.MFCC_BIT
FFT_BIT = prm.FFT_BIT
CQT_BIT = prm.CQT_BIT

TO_SAVE_BMP = prm.TO_SAVE_BMP
TO_SHOW_BMP = prm.TO_SHOW_BMP
TO_SAVE_PYP = prm.TO_SAVE_PYP
TO_SHOW_PYP = prm.TO_SHOW_PYP

# TODO : linker avec unity pour un affichage en 3D de la structure


def graph_algo_cogn(path, path_results, matrix, nb_mfcc, data_length, teta, hop_length, init):
    """ Plot the picture of the formal diagram."""
    name = path.split('/')[-1]
    file_name = name + "_hoplength" + str(hop_length) + "_teta" + str(teta) + "_init" + str(init)
    file_name_cv2 = file_name_pyplot = ''
    title = "Diagramme formel de " + name + "  teta" + str(teta) + " hoplength" + str(hop_length) + " init" + str(init)
    if MFCC_BIT:
        file_name_cv2 = "diagcog-mfcc_" + file_name + "_mfcc" + str(nb_mfcc) + ".bmp"
        file_name_pyplot = "diagcog-mfcc_" + file_name + "_mfcc" + str(nb_mfcc) + ".png"
        title = title + " mfcc" + str(nb_mfcc)
    elif FFT_BIT:
        file_name_cv2 = "diagcog-fft_" + file_name + ".bmp"
        file_name_pyplot = "diagcog-fft_" + file_name + ".png"
    elif CQT_BIT:
        file_name_cv2 = "diagcog-cqt_" + file_name + ".bmp"
        file_name_pyplot = "diagcog-cqt_" + file_name + ".png"

    if TO_SHOW_BMP:
        cv2.imshow(title, matrix)
        cv2.waitKey()
    if TO_SAVE_BMP:
        cv2.imwrite(path_results + file_name_cv2, matrix)

    matrix = cv2.cvtColor(matrix, cv2.COLOR_BGR2RGB)
    plt.figure(figsize=(32, 20))
    plt.title(title)
    plt.xlabel("temps (mémoire forme)")
    plt.ylabel("matériau (mémoire matériau)")
    plt.imshow(matrix, extent=[0, data_length, len(matrix), 0])
    if TO_SAVE_PYP:
        plt.savefig(path_results + file_name_pyplot)
    if TO_SHOW_PYP:
        plt.show()
    plt.close()
