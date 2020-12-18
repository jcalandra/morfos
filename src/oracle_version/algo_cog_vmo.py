import data_computing as dc
import sim_functions as sf
import parameters as prm
import numpy as np
import cv2
import time
import oracle_ac
import plot
import synthesis_vmo as svmo

# TODO !!! : changer tous les del et toutes les modifications de matrices pour les faire passer en numpy array

# TODO : intégrer le timbre dans la représentation
# TODO : intégrer une hiérarchisation

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
SUFFIX_METHOD = prm.SUFFIX_METHOD
FMIN = prm.NOTE_MIN


def modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data):
    obs = input_data[i_hop]
    if prev_mat == oracle_t.data[-1]:
        if len(oracle_t.latent[prev_mat]) > 1:
            good_sfx = oracle_t.latent[prev_mat][-2]
        else:
            good_sfx = 0
    else:
        good_sfx = oracle_t.latent[prev_mat][-1]
    oracle_t.data[i_hop + 1] = prev_mat
    oracle_t.rsfx[oracle_t.sfx[i_hop + 1]].pop()
    oracle_t.rsfx[good_sfx].append(i_hop + 1)
    (oracle_t.rsfx[good_sfx]).sort()

    oracle_t.rep[prev_mat][0] = (oracle_t.rep[prev_mat][0] * oracle_t.rep[prev_mat][1] + obs) / \
                                (oracle_t.rep[prev_mat][1] + 1)
    oracle_t.rep[prev_mat][1] = oracle_t.rep[prev_mat][1] + 1
    oracle_t.sfx[i_hop + 1] = good_sfx
    oracle_t.latent[j_mat].pop()
    oracle_t.latent[prev_mat].append(i_hop + 1)
    (oracle_t.latent[prev_mat]).sort()

    if (oracle_t.rep[j_mat][0] * oracle_t.rep[j_mat][1] - obs).all() == 0 and oracle_t.rep[j_mat][1] - 1 == 0:
        oracle_t.rep.pop(j_mat)
        oracle_t.latent.pop(j_mat)
        for j in range(len(oracle_t.data) - 2, len(oracle_t.data)):
            if oracle_t.data[j] and oracle_t.data[j] > j_mat:
                oracle_t.data[j] = oracle_t.data[j] - 1
    else:
        oracle_t.rep[j_mat][0] = (oracle_t.rep[j_mat][0] * oracle_t.rep[j_mat][1] - obs) / \
                             (oracle_t.rep[j_mat][1] - 1)
        oracle_t.rep[j_mat][1] = oracle_t.rep[j_mat][1] - 1


def modify2_oracle(oracle_t, prev2_mat, prev_mat, j_mat, i_hop, input_data):
    obs_1 = input_data[i_hop]
    obs_2 = input_data[i_hop - 1]

    if prev2_mat == oracle_t.data[-1]:
        if len(oracle_t.latent[prev2_mat]) > 1:
            good_sfx = oracle_t.latent[prev2_mat][-2]
        else:
            good_sfx = 0
    else:
        good_sfx = oracle_t.latent[prev2_mat][-1]

    oracle_t.data[i_hop + 1] = prev2_mat
    oracle_t.data[i_hop] = prev2_mat

    oracle_t.rsfx[oracle_t.sfx[i_hop + 1]].pop()
    oracle_t.rsfx[oracle_t.sfx[i_hop]].pop()
    oracle_t.rsfx[good_sfx - 1].append(i_hop)
    oracle_t.rsfx[good_sfx].append(i_hop + 1)
    (oracle_t.rsfx[good_sfx - 1]).sort()
    (oracle_t.rsfx[good_sfx]).sort()

    oracle_t.rep[prev2_mat][0] = (oracle_t.rep[prev2_mat][0] * oracle_t.rep[prev2_mat][1] + obs_2) / \
                                 (oracle_t.rep[prev2_mat][1] + 1)
    oracle_t.rep[prev2_mat][1] = oracle_t.rep[prev2_mat][1] + 1
    oracle_t.rep[prev2_mat][0] = (oracle_t.rep[prev2_mat][0] * oracle_t.rep[prev2_mat][1] + obs_1) / \
                                 (oracle_t.rep[prev2_mat][1] + 1)
    oracle_t.rep[prev2_mat][1] = oracle_t.rep[prev2_mat][1] + 1

    oracle_t.sfx[i_hop] = good_sfx - 1
    oracle_t.sfx[i_hop + 1] = good_sfx

    oracle_t.latent[j_mat].pop()
    oracle_t.latent[prev_mat].pop()
    oracle_t.latent[prev2_mat].append(i_hop)
    oracle_t.latent[prev2_mat].append(i_hop + 1)
    (oracle_t.latent[prev2_mat]).sort()
    if prev_mat != j_mat and (oracle_t.rep[j_mat][0] * oracle_t.rep[j_mat][1] - obs_1).all() == 0:
        oracle_t.rep.pop(j_mat)
        oracle_t.latent.pop(j_mat)
        if prev_mat > j_mat:
            prev_mat = prev_mat - 1
        for j in range(len(oracle_t.data) - 3, len(oracle_t.data)):
            if oracle_t.data[j] and oracle_t.data[j] > j_mat:
                oracle_t.data[j] = oracle_t.data[j] - 1
    else:
        oracle_t.rep[j_mat][0] = (oracle_t.rep[j_mat][0] * oracle_t.rep[j_mat][1] - obs_1) / \
                                 (oracle_t.rep[j_mat][1] - 1)
        oracle_t.rep[j_mat][1] = oracle_t.rep[j_mat][1] - 1
    if (oracle_t.rep[prev_mat][0] * oracle_t.rep[prev_mat][1] - obs_2).all() == 0:
        oracle_t.rep.pop(prev_mat)
        oracle_t.latent.pop(prev_mat)
        for j in range(len(oracle_t.data) - 3, len(oracle_t.data)):
            if oracle_t.data[j] and oracle_t.data[j] > prev_mat:
                oracle_t.data[j] = oracle_t.data[j] - 1
    else:
        oracle_t.rep[prev_mat][0] = (oracle_t.rep[prev_mat][0] * oracle_t.rep[prev_mat][1] - obs_2) / \
                                    (oracle_t.rep[prev_mat][1] - 1)
        oracle_t.rep[prev_mat][1] = oracle_t.rep[prev_mat][1] - 1


def algo_cog(audio_path, hop_length, nb_values, teta, init, fmin=FMIN):
    """ Compute the formal diagram of the audio at audio_path with threshold teta and size of frame hop_length."""
    print("[INFO] Computing the cognitive algorithm of the audio extract...")
    here_time = time.time()

    data, rate, data_size, data_length = dc.get_data(audio_path)
    temps_data = time.time() - here_time
    print("Temps data : %s secondes ---" % temps_data)

    nb_points = NB_SILENCE
    a = np.zeros(nb_points)
    data = np.concatenate((a, data))

    # initialise matrix of each hop coordinates
    nb_sil_frames = nb_points/hop_length
    nb_hop = int(data_size/hop_length + nb_sil_frames) + 1
    data_length = data_length + nb_points/rate
    if data_size % hop_length < init:
        nb_hop = int(data_size/hop_length)
    print("[RESULT] audio length = ", nb_hop)

    new_mat = np.ones((1, nb_hop, 3), np.uint8)
    for i in range(nb_hop):
        new_mat[0][i] = BACKGROUND
    mtx = new_mat.copy()

    temps_sup = time.time() - here_time
    print("Temps sup : %s secondes ---" % temps_sup)

    print("[INFO] Computing frequencies and volume...")
    v_tab, s_tab = dc.get_descriptors(data, rate, hop_length, nb_hop, nb_values, init, fmin)

    value = 255 - v_tab[0] * 255
    color = (BASIC_FRAME[0], BASIC_FRAME[1], value)
    mtx[0][0] = color

    seg_error = 0
    class_error = 0

    print("[INFO] Computing formal diagram...")

    start_time = time.time()

    # ------- CREATE AND BUILD ORACLE -------

    weights = None
    feature = None

    flag = 'a'
    threshold = teta
    dfunc = 'cosine'
    dfunc_handle = None
    if prm.MFCC_BIT == 1:
        dim = nb_values - 1
    elif prm.FFT_BIT == 1:
        dim = nb_hop
    else:
        dim = nb_values

    if prm.FFT_BIT == 1:
        input_data = np.array(s_tab).transpose()
    else:
        input_data = s_tab.transpose()

    volume_data = v_tab
    suffix_method = SUFFIX_METHOD

    r = (0.00, 1.01, 0.01)
    # ideal_t = oracle.find_threshold(input_data, r=r, flag='a', dim=nb_values)
    # print(ideal_t[0][1])

    if weights is None:
        weights = {}
        weights.setdefault(feature, 1.0)

    if type(input_data) != np.ndarray or type(input_data[0]) != np.ndarray:
        input_data = np.array(input_data)
    if input_data.ndim != 2:
        input_data = np.expand_dims(input_data, axis=1)

    if flag == 'f' or flag == 'v':
        oracle_t = oracle_ac.create_oracle(flag, threshold=threshold, dfunc=dfunc, dfunc_handle=dfunc_handle, dim=dim)

    else:
        oracle_t = oracle_ac.create_oracle('a', threshold=threshold, dfunc=dfunc, dfunc_handle=dfunc_handle, dim=dim)

    prev_mat = prev2_mat = prev3_mat = 0
    actual_max = temp_max = 0
    temp_mat = new_mat = 0
    color = color2 = color3 = (BASIC_FRAME[0], BASIC_FRAME[1], v_tab[0])

    for i_hop in range(nb_hop):  # while
        obs = input_data[i_hop]
        if flag == 'f' or flag == 'v':
            oracle_t.add_state(obs)
        else:
            oracle_t.add_state(obs, input_data, volume_data, suffix_method)

        j_mat = oracle_t.data[i_hop + 1]
        value = 255 - v_tab[i_hop]*255
        color3 = color2
        color2 = color
        color = (BASIC_FRAME[0], BASIC_FRAME[1], value)

        # faire passer SEGMENTATION_BIT en argument de la fonction pour pouvoir choisir à chaque étape de l'algorithme.
        if SEGMENTATION_BIT:
            diff = sf.dissimilarity(i_hop, s_tab, v_tab)
            if diff:
                color = SEGMENTATION

        if i_hop > 2:
            prev_mat = oracle_t.data[i_hop]
            prev2_mat = oracle_t.data[i_hop - 1]
            prev3_mat = oracle_t.data[i_hop - 2]

        if i_hop == nb_hop - 1 and j_mat != prev_mat:
            print("last frame")
            modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data)
            j_mat = prev_mat

        if j_mat > actual_max:

            # faire passer CORRECTION_BIT en argument de la fonction pour pouvoir choisir à chaque étape de l'algorithme
            if i_hop > 2 and prev_mat != prev2_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                seg_error = seg_error + 1
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 2,  j_mat, prev2_mat, s_tab)
                if good_mat == j_mat:
                    modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data)
                    j_mat = oracle_t.data[i_hop]
                    temp_max = j_mat

                else:
                    modify_oracle(oracle_t, prev2_mat, prev_mat, i_hop - 1, input_data)

            elif i_hop > 2 and prev_mat != prev3_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 3, j_mat, prev3_mat, s_tab)
                if good_mat == j_mat:
                    modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data)
                    j_mat = oracle_t.data[i_hop]
                    temp_max = j_mat
                    seg_error = seg_error + 1
                else:
                    modify2_oracle(oracle_t, prev3_mat, prev2_mat, prev_mat, i_hop - 1, input_data)
                    seg_error = seg_error + 2

        if j_mat > actual_max:
            temp_max = j_mat
            new_mat_l = np.ones((1, nb_hop, 3), np.uint8)
            for i in range(nb_hop):
                new_mat_l[0][i] = BACKGROUND
            mtx = np.concatenate((mtx, new_mat_l))

        else:

            if i_hop > 2 and prev_mat != prev2_mat and j_mat != prev_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 1
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 2, j_mat, prev2_mat, s_tab)

                # ici, on dit que le meilleur est le précédent par défaut (car on ne peut pas pointer un suffixe vers
                # l'élément suivant
                modify_oracle(oracle_t, good_mat, prev_mat, i_hop - 1, input_data)

            if i_hop > 2 and prev_mat == prev2_mat and prev_mat != prev3_mat and j_mat != prev_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 2
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 3, j_mat, prev3_mat, s_tab)
                modify2_oracle(oracle_t, good_mat, prev2_mat, prev_mat, i_hop - 1, input_data)

        for j in range(len(oracle_t.data) - 3, len(oracle_t.data)):
            for k in range(len(mtx)):
                mtx[k][j - 1] = BACKGROUND
        mtx[oracle_t.data[j - 2]][j - 3] = color3
        mtx[oracle_t.data[j - 1]][j - 2] = color2
        mtx[oracle_t.data[j]][j - 1] = color

        if temp_max > actual_max:
            actual_max = temp_max

    while len(oracle_t.rep) < len(mtx):
        mtx = np.delete(mtx, - 1, 0)
    if flag != 'f' and flag != 'v':
        oracle_t.f_array.finalize()

    mtx = cv2.cvtColor(mtx, cv2.COLOR_HSV2BGR)
    distance = (seg_error + class_error)/nb_hop

    algocog_time = time.time() - start_time
    print("Temps de calcul l'algorithme : %s secondes ---" % algocog_time)
    '''f_ac = open("../../results/algocog_computing.txt", "a")
    f_ac.write(str(algocog_time) + "\n")
    f_ac.close()'''

    if WRITE_RESULTS:
        name = audio_path.split('/')[-1]
        file = open("../results/error.txt", "a")
        file.write("\nERROR file " + name + ", " + str(hop_length) + ", " + str(nb_values) + ", " + str(teta) +
                   ", " + str(init) + "\nseg_error = " + str(seg_error) + "\nclass_error = " + str(class_error) +
                   "\ndistance = " + str(distance) + "\n")
        file.close()
    print("seg error =", seg_error)
    print("class error =", class_error)
    print(oracle_t.data)
    # name = audio_path.split('/')[-1][:-4] + '_synthesis.wav'
    # print(name)
    # svmo.synthesis(oracle_t, nb_hop, data, hop_length, rate, name)
    # im = plot.start_draw(oracle_t, size=(900 * 4, 400 * 4))
    # im.show()
    t = time.time() - here_time
    print("temps total total :", t)
    return mtx, data_length, data_size, distance, t
