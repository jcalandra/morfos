import data_computing as dc
import similarity_functions as sf
import parameters as prm
import numpy as np
import cv2
import time_manager

# In this file are implemented functions for the cognitive algorithm at level 0: the signal scale, in this most standard
# version

# note : matrices are created in HSV
D_THRESHOLD = prm.D_THRESHOLD
BASIC_FRAME = prm.BASIC_FRAME
BACKGROUND = prm.BACKGROUND
SEGMENTATION = prm.SEGMENTATION
SEG_ERROR = prm.SEG_ERROR
CLASS_ERROR = prm.CLASS_ERROR

CORRECTION_BIT = prm.CORRECTION_BIT
CORRECTION_BIT_COLOR = prm.CORRECTION_BIT_COLOR
SEGMENTATION_BIT = prm.SEGMENTATION_BIT
WRITE_RESULTS = prm.WRITE_RESULTS

NB_SILENCE = prm.NB_SILENCE
FMIN = prm.NOTE_MIN


# ============================== STANDARD COGNITIVE ALGORITHM AT SIGNAL SCALE ==========================================
def algo_cog(audio_path, hop_length, nb_mfcc, teta, init, fmin=FMIN):
    """ Compute the formal diagram of the audio at audio_path with threshold teta and size of frame hop_length."""
    print("[INFO] Computing the cognitive algorithm of the audio extract...")
    here_time = time_manager.time()

    data, rate, data_size, data_length = dc.get_data(audio_path)
    nb_points = NB_SILENCE
    a = np.zeros(nb_points)
    data = np.concatenate((a, data))
    # initialise matrix of each hop coordinates
    mat = [0]  # matrix where each accessor correspond to state and each result is the adequate material
    nb_mat = 1  # number of materials
    nb_sil_frames = nb_points/hop_length
    nb_hop = int(data_size/hop_length + nb_sil_frames) + 1  # nb of hop, not supposed to be known it in realtime
    data_length = data_length + nb_points/rate
    if data_size % hop_length < init:
        nb_hop = int(data_size/hop_length)
    print("[RESULT] audio length = ", nb_hop)

    new_mat = np.ones((1, nb_hop, 3), np.uint8)
    for i in range(nb_hop):
        new_mat[0][i] = BACKGROUND
    mtx = new_mat.copy()

    print("[INFO] Computing frequencies and volume...")
    v_tab, s_tab = dc.get_descriptors(data, rate, hop_length, nb_hop, nb_mfcc, init, fmin)

    value = 255 - v_tab[0] * 255
    color = (BASIC_FRAME[0], BASIC_FRAME[1], value)
    mtx[0][0] = color

    seg_error = 0
    class_error = 0

    print("[INFO] Computing formal diagram...")

    start_time = time_manager.time()

    for i_hop in range(1, nb_hop):
        j_mat = sf.comparison(i_hop, teta, s_tab, v_tab, mat, audio_path)
        prev_mat = prev2_mat = prev3_mat = 0
        value = 255 - v_tab[i_hop]*255
        color = (BASIC_FRAME[0], BASIC_FRAME[1], value)

        if SEGMENTATION_BIT:
            diff = sf.dissimilarity(i_hop, s_tab, v_tab)
            if diff:
                color = SEGMENTATION

        if i_hop > 2:
            prev_mat = mat[i_hop - 1]
            prev2_mat = mat[i_hop - 2]
            prev3_mat = mat[i_hop - 3]

        if i_hop == nb_hop - 1 and j_mat != prev_mat:
            j_mat = prev_mat

        if j_mat == -1:
            if i_hop > 2 and prev_mat != prev2_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                seg_error = seg_error + 1
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 2,  j_mat, prev2_mat, s_tab)
                if good_mat == j_mat:
                    j_mat = prev_mat
                else:
                    mtx[prev_mat][i_hop - 1] = BACKGROUND
                    mtx[prev2_mat][i_hop - 1] = color
                    mat[i_hop - 1] = prev2_mat

            elif i_hop > 2 and prev_mat != prev3_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 3, j_mat, prev3_mat, s_tab)
                if good_mat == j_mat:
                    j_mat = prev_mat
                    seg_error = seg_error + 1
                else:
                    mtx[prev_mat][i_hop - 1] = BACKGROUND
                    mtx[prev2_mat][i_hop - 2] = BACKGROUND
                    mtx[prev3_mat][i_hop - 1] = color
                    mtx[prev3_mat][i_hop - 2] = color
                    mat[i_hop - 1] = prev3_mat
                    mat[i_hop - 2] = prev3_mat
                    seg_error = seg_error + 2

            if j_mat == -1:
                nb_mat = nb_mat + 1
                mat.append(nb_mat - 1)
                new_mat = np.ones((1, nb_hop, 3), np.uint8)
                for i in range(nb_hop):
                    new_mat[0][i] = BACKGROUND
                mtx = np.concatenate((mtx, new_mat))
                mtx[nb_mat - 1][i_hop] = color

        if j_mat != -1:
            mat.append(j_mat)
            mtx[j_mat][i_hop] = color

            if i_hop > 2 and prev_mat != prev2_mat and j_mat != prev_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 1
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 2, j_mat, prev2_mat, s_tab)

                mtx[prev_mat][i_hop - 1] = BACKGROUND
                mtx[good_mat][i_hop - 1] = color

                mat[i_hop - 1] = good_mat

            if i_hop > 2 and prev_mat == prev2_mat and prev_mat != prev3_mat and j_mat != prev_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 2
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 3, j_mat, prev3_mat, s_tab)

                mtx[prev_mat][i_hop - 1] = BACKGROUND
                mtx[prev2_mat][i_hop - 2] = BACKGROUND
                mtx[good_mat][i_hop - 1] = color
                mtx[good_mat][i_hop - 2] = color

                mat[i_hop - 1] = good_mat
                mat[i_hop - 2] = good_mat

    i = 0
    k = 0
    while i < len(mtx):
        j = 0
        while j < len(mat) and i + k != mat[j]:
            j = j + 1
        if j == len(mat):
            mtx = np.delete(mtx, i, axis=0)
            k = k + 1
        else:
            i = i + 1

    mtx = cv2.cvtColor(mtx, cv2.COLOR_HSV2BGR)
    distance = (seg_error + class_error)/nb_hop

    algocog_time = time_manager.time() - start_time
    '''print("Temps de calcul l'algorithme : %s secondes ---" % algocog_time)
    f_ac = open("../results/algocog_computing.txt", "a")
    f_ac.write(str(algocog_time) + "\n")
    f_ac.close()'''

    if WRITE_RESULTS:
        name = audio_path.split('/')[-1]
        file = open("../results/error.txt", "a")
        file.write("\nERROR file " + name + ", " + str(hop_length) + ", " + str(nb_mfcc) + ", " + str(teta) +
                   ", " + str(init) + "\nseg_error = " + str(seg_error) + "\nclass_error = " + str(class_error) +
                   "\ndistance = " + str(distance) + "\n")
        file.close()
    print("seg error =", seg_error)
    print("class error =", class_error)
    t = time_manager.time() - here_time
    print("temps total :", t)
    return mtx, data_length, data_size, distance, t
