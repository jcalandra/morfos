import data_computing as dc
import similarity_functions as sf
import parameters as prm
import numpy as np
import cv2


# In this file are implemented functions for the cognitive algorithm at level 0: the signal scale, with a representant
# for each material

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


# ======================================= REPRESENTANT MATRIX UPDATES ==================================================
def update_mat_rep(mat_rep, j_mat, i_hop, s_tab, v_tab):
    """ Update the representant matrix mat_rep with the new object of material j_mat."""
    if v_tab[i_hop] == 0:
        s = s_tab[i_hop]
    else:
        s = s_tab[i_hop] / v_tab[i_hop]
    mat_rep[j_mat][1] = mat_rep[j_mat][1] + 1
    nb_rep = mat_rep[j_mat][1]
    for i in range(len(mat_rep[j_mat][0])):
        mat_rep[j_mat][0][i] = (mat_rep[j_mat][0][i] * (nb_rep - 1) + s[i]) / nb_rep
    return mat_rep


# ============================ COGNITIVE ALGORITHM AT SIGNAL SCALE WITH REPRESENTANTS===================================
def algo_cog(audio_path, hop_length, nb_mfcc, teta, init, fmin=FMIN):
    """ Compute the formal diagram of the audio at audio_path with threshold teta and size of frame hop_length."""
    print("[INFO] Computing the cognitive algorithm of the audio extract...")
    data, rate, data_size, data_length = dc.get_data(audio_path)
    nb_points = NB_SILENCE
    a = np.zeros(nb_points)
    data = np.concatenate((a, data))
    # initialise matrix of each hop coordinates
    nb_hop = int(data_size/hop_length + nb_points/hop_length) + 1  # nb of hop, not supposed to be known it in realtime
    if data_size % hop_length < init:
        nb_hop = int(data_size/hop_length)
    print("[RESULT] audio length = ", nb_hop)

    new_mat = np.ones((1, nb_hop, 3), np.uint8)
    for i in range(nb_hop):
        new_mat[0][i] = BACKGROUND
    mtx = new_mat.copy()

    print("[INFO] Computing frequencies and volume...")
    v_tab, s_tab = dc.get_descriptors(data, rate, hop_length, nb_hop, nb_mfcc, init, fmin)

    mat = [0]  # matrix where each accessor correspond to state and each result is the adequate material
    if v_tab[0] == 0:
        s = s_tab[0]
    else:
        s = s_tab[0]/v_tab[0]
    mat_rep = [[s, 1]]  # matrix where each accessor correspond to number of material and each result is
    mat_rep_null = [[0 for i in range(len(s_tab[0]))], 0]
    mat_rep_prev = mat_rep_prev2 = mat_rep_prev3 = []
    # the couple (representant of material, nb of constituants)
    nb_mat = 1  # number of materials

    value = 255 - v_tab[0] * 255
    color = (BASIC_FRAME[0], BASIC_FRAME[1], value)
    mtx[0][0] = color

    seg_error = 0
    class_error = 0

    print("[INFO] Computing formal diagram...")

    # start_time = time.time()

    for i_hop in range(1, nb_hop):  # while
        j_mat = sf.comparison_rep(i_hop, teta, s_tab, v_tab, mat_rep)
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

        if j_mat == -1:
            if i_hop > 2 and prev_mat != prev2_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                seg_error = seg_error + 1
                good_mat = sf.true_mat_rep(mat_rep[mat[i_hop - 1]][0], s_tab[i_hop], mat_rep[mat[i_hop - 2]][0],
                                           j_mat, prev2_mat)

                if good_mat == j_mat:
                    j_mat = prev_mat
                else:  # good_mat = prev2_mat
                    mtx[prev_mat][i_hop - 1] = BACKGROUND
                    mtx[prev2_mat][i_hop - 1] = color

                    # update of mat_rep
                    if mat_rep[prev_mat][1] > 1:
                        mat_rep[prev_mat] = mat_rep_prev2[mat[i_hop - 1]]
                    else:
                        mat_rep[prev_mat] = mat_rep_null

                    mat_rep = update_mat_rep(mat_rep, prev2_mat, i_hop - 1, s_tab, v_tab)

                    mat[i_hop - 1] = prev2_mat

            elif i_hop > 2 and prev_mat != prev3_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                good_mat = sf.true_mat_rep(mat_rep[mat[i_hop - 1]][0], s_tab[i_hop], mat_rep[mat[i_hop - 3]][0],
                                           j_mat, prev3_mat)

                if good_mat == j_mat:
                    j_mat = prev_mat
                    seg_error = seg_error + 1
                else:
                    mtx[prev_mat][i_hop - 1] = BACKGROUND
                    mtx[prev2_mat][i_hop - 2] = BACKGROUND
                    mtx[prev3_mat][i_hop - 1] = color
                    mtx[prev3_mat][i_hop - 2] = color

                    # update of mat_rep
                    if mat_rep[prev_mat][1] > 1:
                        mat_rep[prev_mat] = mat_rep_prev2[prev_mat]
                    else:
                        mat_rep[prev_mat] = mat_rep_null
                    if mat_rep[prev2_mat][1] > 1:
                        mat_rep[prev2_mat] = mat_rep_prev3[prev2_mat]
                    else:
                        mat_rep[prev2_mat] = mat_rep_null

                    mat_rep = update_mat_rep(mat_rep, prev3_mat, i_hop - 1, s_tab, v_tab)
                    mat_rep = update_mat_rep(mat_rep, prev3_mat, i_hop - 2, s_tab, v_tab)

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
                # Creation of a new mat_rep
                new_rep = [s_tab[i_hop], 1]
                mat_rep.append(new_rep)

        if j_mat != -1:
            mtx[j_mat][i_hop] = color
            # update of mat_rep

            mat_rep = update_mat_rep(mat_rep, j_mat, i_hop, s_tab, v_tab)
            mat.append(j_mat)

            if i_hop > 2 and prev_mat != prev2_mat and j_mat != prev_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 1
                good_mat = sf.true_mat_rep(mat_rep[mat[i_hop - 1]][0], s_tab[i_hop], mat_rep[mat[i_hop - 2]][0],
                                           j_mat, prev2_mat)

                mtx[prev_mat][i_hop - 1] = BACKGROUND
                mtx[good_mat][i_hop - 1] = color

                # update of mat_rep
                if mat_rep[prev_mat][1] > 1:
                    mat_rep[prev_mat] = mat_rep_prev2[prev_mat]
                else:
                    mat_rep[prev_mat] = mat_rep_null

                mat_rep = update_mat_rep(mat_rep, good_mat, i_hop - 1, s_tab, v_tab)
                mat[i_hop - 1] = good_mat

            elif i_hop > 2 and prev_mat != prev3_mat and j_mat != prev_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 2
                good_mat = sf.true_mat_rep(mat_rep[mat[i_hop - 1]][0], s_tab[i_hop], mat_rep[mat[i_hop - 3]][0],
                                           j_mat, prev3_mat)

                mtx[prev_mat][i_hop - 1] = BACKGROUND
                mtx[prev2_mat][i_hop - 2] = BACKGROUND
                mtx[good_mat][i_hop - 1] = color
                mtx[good_mat][i_hop - 2] = color

                # update of mat_rep
                if mat_rep[prev_mat][1] > 1:
                    mat_rep[prev_mat] = mat_rep_prev2[prev_mat]
                else:
                    mat_rep[prev_mat] = mat_rep_null
                if mat_rep[prev2_mat][1] > 1:
                    mat_rep[prev2_mat] = mat_rep_prev3[prev2_mat]
                else:
                    mat_rep[prev2_mat] = mat_rep_null

                mat_rep = update_mat_rep(mat_rep, good_mat, i_hop - 1, s_tab, v_tab)
                mat_rep = update_mat_rep(mat_rep, good_mat, i_hop - 2, s_tab, v_tab)

                mat[i_hop - 1] = good_mat
                mat[i_hop - 2] = good_mat

        mat_rep_prev3 = np.copy(mat_rep_prev2)
        mat_rep_prev2 = np.copy(mat_rep_prev)
        mat_rep_prev = np.copy(mat_rep)

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

    if WRITE_RESULTS:
        name = audio_path.split('/')[-1]
        file = open("../results/error.txt", "a")
        file.write("\nERROR file " + name + ", " + str(hop_length) + ", " + str(nb_mfcc) + ", " + str(teta) +
                   ", " + str(init) + "\nseg_error = " + str(seg_error) + "\nclass_error = " + str(class_error) +
                   "\ndistance = " + str(distance) + "\n")
        file.close()

    return mtx, data_length, data_size, distance
