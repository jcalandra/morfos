import data_computing as dc
import similarity_functions as sf
import similarity_rules as sim_rules
import parameters as prm
import numpy as np
import cv2
import time
import plot

import class_mso
import class_s_mso
import class_cog_algo

# In this file are implemented functions for the cognitive algorithm  with the oracle as the main structure

# TODO : intégrer le timbre dans la représentation

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
fmin = prm.NOTE_MIN

SYNTHESIS = prm.SYNTHESIS
PLOT_ORACLE = prm.PLOT_ORACLE

hop_length = prm.HOP_LENGTH
init = prm.INIT
nb_values = prm.NB_VALUES
teta = prm.TETA
letter_diff = prm.LETTER_DIFF


# ======================================== ORACLE INITIALISATION AND CORRECTION ========================================
def modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data):
    """ Modify the oracle 'oracle_t' according to the last corrected frame of mat 'j_mat' at instant 'i_hop'."""
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
        oracle_t.vec.pop(j_mat - 1)
        for ind in range(j_mat - 1, len(oracle_t.vec)):
            oracle_t.vec[ind].pop(prev_mat - 1)
        for j in range(len(oracle_t.data) - 2, len(oracle_t.data)):
            if oracle_t.data[j] and oracle_t.data[j] > j_mat:
                oracle_t.data[j] = oracle_t.data[j] - 1
    else:
        oracle_t.rep[j_mat][0] = (oracle_t.rep[j_mat][0] * oracle_t.rep[j_mat][1] - obs) / \
                                 (oracle_t.rep[j_mat][1] - 1)
        oracle_t.rep[j_mat][1] = oracle_t.rep[j_mat][1] - 1


def modify2_oracle(oracle_t, prev2_mat, prev_mat, j_mat, i_hop, input_data):
    """ Modify the oracle 'oracle_t' according to the two last corrected frames of mat 'j_mat' and 'prev_mat' at instant
    'i_hop' and i_hop - 1."""
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
        oracle_t.vec.pop(j_mat - 1)
        for ind in range(j_mat - 1, len(oracle_t.vec)):
            oracle_t.vec[ind].pop(prev_mat - 1)
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
        oracle_t.vec.pop(prev_mat - 1)
        for ind in range(prev_mat - 1, len(oracle_t.vec)):
            oracle_t.vec[ind].pop(prev_mat - 1)
        for j in range(len(oracle_t.data) - 3, len(oracle_t.data)):
            if oracle_t.data[j] and oracle_t.data[j] > prev_mat:
                oracle_t.data[j] = oracle_t.data[j] - 1
    else:
        oracle_t.rep[prev_mat][0] = (oracle_t.rep[prev_mat][0] * oracle_t.rep[prev_mat][1] - obs_2) / \
                                    (oracle_t.rep[prev_mat][1] - 1)
        oracle_t.rep[prev_mat][1] = oracle_t.rep[prev_mat][1] - 1


def dims_oracle(nb_values, s_tab, v_tab):
    """Initialize an oracle with the given parameters."""
    volume_data = v_tab
    suffix_method = SUFFIX_METHOD

    if prm.MFCC_BIT == 1:
        dim = nb_values - 1
        input_data = s_tab.transpose()
    elif prm.FFT_BIT == 1:
        dim = len(s_tab[0])
        input_data = np.array(s_tab)
    else:
        dim = nb_values
        input_data = s_tab.transpose()

    if type(input_data) != np.ndarray or type(input_data[0]) != np.ndarray:
        input_data = np.array(input_data)
    if input_data.ndim != 2:
        input_data = np.expand_dims(input_data, axis=1)

    return volume_data, suffix_method, input_data, dim


# ================================================ MATRIX CORRECTION ===================================================
def modify_matrix(mtx, prev_mat, matrix, actual_max, temp_max, lim_ind):
    """ Modify the similarity matrix according the the corrected frames."""
    # TODO: regarder les ajouts et suppression dans oracle_t.vec
    blank_ind = 0
    while mtx[prev_mat][blank_ind][0] == BACKGROUND[0] and mtx[prev_mat][blank_ind][1] == BACKGROUND[1] \
            and mtx[prev_mat][blank_ind][2] == BACKGROUND[2]:
        blank_ind += 1

    if blank_ind == lim_ind and prev_mat == actual_max:
        matrix[0] = matrix[0][:-1]
        matrix[1].pop()
        for i in range(len(matrix[1])):
            matrix[1][i].pop()
        actual_max = actual_max - 1
        temp_max = temp_max - 1
        mtx = np.delete(mtx, - 1, 0)
        return 1, actual_max, temp_max, mtx
    return 0, actual_max, temp_max, mtx


# ============================================ COGNITIVE ALGORITHM =====================================================
def df_init(ms_oracle, nb_points):
    """ Initialize the structure corresponding to the formal diagram of level 0."""
    # initialise matrix of each hop coordinates
    data_size = ms_oracle.data_size
    data_length = ms_oracle.data_length
    rate = ms_oracle.rate

    nb_sil_frames = nb_points / hop_length
    nb_hop = int(data_size / hop_length + nb_sil_frames) + 1
    data_length = data_length + nb_points / rate
    if data_size % hop_length < init:
        nb_hop = int(data_size / hop_length)
    if prm.verbose == 1:
        print("[RESULT] audio length = ", nb_hop)

    new_mat = np.ones((1, nb_hop, 3), np.uint8)
    for i in range(nb_hop):
        new_mat[0][i] = BACKGROUND
    df = new_mat.copy()
    return df, nb_hop, data_length


def algo_cog(audio_path, ms_oracle, end_mk=0):
    """ Compute the formal diagram of the audio at audio_path with threshold teta and size of frame hop_length."""
    print("[INFO] Computing the cognitive algorithm of the audio extract...")
    nb_points = NB_SILENCE
    a = np.zeros(nb_points)
    mtx, nb_hop, data_length = df_init(ms_oracle, nb_points)
    ms_oracle.update_audio(a, data_length, nb_hop)

    if prm.verbose == 1:
        print("[INFO] Computing frequencies and volume...")
    v_tab, s_tab = dc.get_descriptors(ms_oracle.audio, ms_oracle.rate, hop_length, ms_oracle.nb_hop, nb_values, init,
                                      fmin)
    seg_error = 0
    class_error = 0

    if prm.verbose == 1:
        print("[INFO] Structures initialisation...")

    # ------- INITIALISATION OF STRUCTURES -------
    level = 0
    flag = 'a'
    volume_data, suffix_method, input_data, dim = dims_oracle(nb_values, s_tab, v_tab)
    ms_oracle.matrix = [chr(letter_diff + 1), [[1]]]
    class_mso.MSOLevel(ms_oracle)
    ms_oracle.levels[level].materials.sim_matrix.init(chr(letter_diff + 1), [1])
    ms_oracle.levels[level].init_oracle(flag, teta, dim)

    # formal diagram of level 0
    value = 255 - v_tab[0] * 255
    color = (BASIC_FRAME[0], BASIC_FRAME[1], value)
    mtx[0][0] = color
    ms_oracle.levels[level].formal_diagram.init(ms_oracle, level, mtx)

    # ------- ALGORITHM -------
    prev_mat = prev2_mat = prev3_mat = 0
    actual_max = temp_max = 0
    color = color2 = (BASIC_FRAME[0], BASIC_FRAME[1], v_tab[0])
    diff_mk = 0

    if prm.verbose == 1:
        print("[INFO] Computing formal diagram...")

    start_time = time.time()

    # vsd, vdd, vkl, fsd, fdd = cd.compute_dynamics()

    for i_hop in range(nb_hop):  # while
        if prm.verbose == 1:
            print("[INFO] Process in level 0...")
        obs = input_data[i_hop]
        ms_oracle.levels[level].oracle.add_state(obs, input_data, volume_data, suffix_method)
        oracle_t = ms_oracle.levels[level].oracle
        print("concat obj", ms_oracle.levels[level].link)
        print("i_hop", i_hop)
        concat_obj = ms_oracle.levels[level].concat_obj.concat_labels

        j_mat = oracle_t.data[i_hop + 1]
        value = 255 - v_tab[i_hop] * 255

        color3 = color2
        color2 = color
        color = (BASIC_FRAME[0], BASIC_FRAME[1], value)

        if i_hop > 2:
            prev_mat = oracle_t.data[i_hop]
            prev2_mat = oracle_t.data[i_hop - 1]
            prev3_mat = oracle_t.data[i_hop - 2]

        if i_hop == nb_hop - 1 and j_mat != prev_mat:
            modify_oracle(ms_oracle.levels[level].oracle, prev_mat, j_mat, i_hop, input_data)
            oracle_t = ms_oracle.levels[level].oracle
            j_mat = prev_mat

        '''diff = sf.dissimilarity(i_hop, s_tab, v_tab)
        if diff and len(concat_obj) > 3:
            if diff_mk != 1:
                if SEGMENTATION_BIT:
                    color = SEGMENTATION

                if i_hop == nb_hop - 1:
                    end_mk = 1
                    concat_obj = concat_obj + chr(letter_diff + oracle_t.data[i_hop + 1] + 1)
                # link update
                if len(ms_oracle.levels[level]) > level + 1:
                    # node = len(oracles[1][level + 1][0].data)
                    node = max(ms_oracle.levels[level].link) + 1
                else:
                    node = 1
                for ind in range(len(concat_obj)):
                    ms_oracle.levels[level].link.append(node)
                # history_next update
                new_char = sim_rules.char_next_level_similarity(ms_oracle, level)
                # concat_obj update
                concat_obj = ""
                diff_mk = 1
                class_cog_algo.fun_segmentation(ms_oracle, new_char, level=level + 1, end_mk=end_mk)
                if prm.verbose == 1:
                    print("[INFO] Process in level 0...")
        else:
            diff_mk = 0
            if i_hop == nb_hop - 1:
                end_mk = 1
                concat_obj = concat_obj + chr(letter_diff + oracle_t.data[i_hop + 1] + 1)
                # link update
                if len(ms_oracle.levels) > level + 1:
                    node = max(ms_oracle.level[level].link) + 1
                else:
                    node = 1
                for ind in range(len(concat_obj)):
                    ms_oracle.levels[level].link.append(node)
                # history_next update
                new_char = sim_rules.char_next_level_similarity(ms_oracle, level)
                # concat_obj update
                concat_obj = ""
                diff_mk = 1
                class_cog_algo.fun_segmentation(ms_oracle, new_char, level=level + 1, end_mk=end_mk)
                if prm.verbose == 1:
                    print("[INFO] Process in level 0...")'''

        if j_mat > actual_max:

            if i_hop > 2 and prev_mat != prev2_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                seg_error = seg_error + 1
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 2, j_mat, prev2_mat, s_tab)
                if good_mat == j_mat:
                    modify_oracle(ms_oracle.levels[level].oracle, prev_mat, j_mat, i_hop, input_data)
                    oracle_t = ms_oracle.levels[level].oracle
                    j_mat = oracle_t.data[i_hop]

                else:
                    modify_oracle(ms_oracle.levels[level].oracle, prev2_mat, prev_mat, i_hop - 1, input_data)
                    oracle_t = ms_oracle.levels[level].oracle
                    digit, actual_max, temp_max, mtx = \
                        modify_matrix(mtx, prev_mat, ms_oracle.matrix, actual_max, temp_max, i_hop - 1)
                    if digit == 1:
                        j_mat -= 1

            elif i_hop > 2 and prev_mat != prev3_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 3, j_mat, prev3_mat, s_tab)
                if good_mat == j_mat:
                    modify_oracle(ms_oracle.levels[level].oracle, prev_mat, j_mat, i_hop, input_data)
                    oracle_t = ms_oracle.levels[level].oracle
                    j_mat = oracle_t.data[i_hop]
                    temp_max = j_mat
                else:
                    modify2_oracle(ms_oracle.levels[level].oracle, prev3_mat, prev2_mat, prev_mat, i_hop - 1, input_data)
                    oracle_t = ms_oracle.levels[level].oracle
                    digit, actual_max, temp_max, mtx = \
                        modify_matrix(mtx, prev_mat, ms_oracle.matrix, actual_max, temp_max, i_hop - 1)
                    if digit == 1:
                        j_mat -= 1
                    digit, actual_max, temp_max, mtx = \
                        modify_matrix(mtx, prev2_mat, ms_oracle.matrix, actual_max, temp_max, i_hop - 2)
                    if digit == 1:
                        j_mat -= 1
                    seg_error = seg_error + 2

        if j_mat > actual_max:
            temp_max = j_mat
            vec = oracle_t.vec[len(ms_oracle.matrix[0]) - 1].copy()
            vec.append(1)
            ms_oracle.matrix[0] += (chr(len(ms_oracle.matrix[0]) + letter_diff + 1))
            ms_oracle.matrix[1].append(vec)
            for i in range(len(ms_oracle.matrix[1]) - 1):
                ms_oracle.matrix[1][i].append(ms_oracle.matrix[1][len(ms_oracle.matrix[1]) - 1][i])
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

                # By default the best element is the previous one because FO cannot point on future objects
                modify_oracle(ms_oracle.levels[level].oracle, good_mat, prev_mat, i_hop - 1, input_data)
                oracle_t = ms_oracle.levels[level].oracle
                digit, actual_max, temp_max, mtx = \
                    modify_matrix(mtx, prev_mat, ms_oracle.matrix, actual_max, temp_max, i_hop - 1)

            if i_hop > 2 and prev_mat == prev2_mat and prev_mat != prev3_mat and j_mat != prev_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 2
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 3, j_mat, prev3_mat, s_tab)
                modify2_oracle(ms_oracle.levels[level].oracle, good_mat, prev2_mat, prev_mat, i_hop - 1, input_data)
                oracle_t = ms_oracle.levels[level].oracle
                digit, actual_max, temp_max, mtx = \
                    modify_matrix(mtx, prev_mat, ms_oracle.matrix, actual_max, temp_max, i_hop - 1)
                digit, actual_max, temp_max, mtx = \
                    modify_matrix(mtx, prev2_mat, ms_oracle.matrix, actual_max, temp_max, i_hop - 2)

        if i_hop > 3:
            for j in range(len(oracle_t.data) - 3, len(oracle_t.data)):
                for k in range(len(mtx)):
                    mtx[k][j - 1] = BACKGROUND
            mtx[oracle_t.data[i_hop - 1]][i_hop - 2] = color3
            mtx[oracle_t.data[i_hop]][i_hop - 1] = color2
            mtx[oracle_t.data[i_hop + 1]][i_hop] = color

        history_next = ms_oracle.levels[level].materials.history
        if len(concat_obj) == 1:
            if len(history_next) > 0:
                new_history_next_element = history_next[-1][1]
                if ord(history_next[-1][1][-2]) - letter_diff > len(ms_oracle.matrix[0]):
                    tmp_char = history_next[-1][1][-1]
                    new_history_next_element = new_history_next_element[:-2]
                    new_history_next_element += chr(oracle_t.data[i_hop - 1] + letter_diff + 1)
                    new_history_next_element += tmp_char
                if ord(history_next[-1][1][-1]) - letter_diff > len(ms_oracle.matrix[0]):
                    new_history_next_element = new_history_next_element[:-1]
                    new_history_next_element += chr(oracle_t.data[i_hop - 1] + letter_diff + 1)
                history_next[-1] = (history_next[-1][0], new_history_next_element, history_next[-1][2])
            concat_obj = chr(letter_diff + oracle_t.data[i_hop] + 1)

        if len(concat_obj) == 2:
            if len(history_next) > 0:
                new_history_next_element = history_next[-1][1]
                if ord(history_next[-1][1][-1]) - letter_diff > len(ms_oracle.matrix[0]):
                    new_history_next_element = new_history_next_element[:-1]
                    new_history_next_element += chr(oracle_t.data[i_hop - 1] + letter_diff + 1)
                history_next[-1] = (history_next[-1][0], new_history_next_element,  history_next[-1][2])
            concat_obj = chr(letter_diff + oracle_t.data[i_hop - 1] + 1) \
                         + chr(letter_diff + oracle_t.data[i_hop] + 1)
            # TODO: corriger la valeur dans la matrice

        if len(concat_obj) >= 3:
            concat_obj = concat_obj[:len(concat_obj) - 2] + chr(letter_diff + oracle_t.data[i_hop - 1] + 1) \
                         + chr(letter_diff + oracle_t.data[i_hop] + 1)
        concat_obj = concat_obj + chr(letter_diff + oracle_t.data[i_hop + 1] + 1)

        if temp_max > actual_max:
            actual_max = temp_max
        formal_diagram = cv2.cvtColor(mtx, cv2.COLOR_HSV2BGR)
        ms_oracle.levels[level].formal_diagram_graph.update(ms_oracle, level)

        ms_oracle.levels[level].materials.history = history_next
        ms_oracle.levels[level].concat_obj.concat_labels = concat_obj
        ms_oracle.levels[level].formal_diagram.material_lines = formal_diagram

    if flag != 'f' and flag != 'v':
        ms_oracle.levels[level].oracle.f_array.finalize()

    mtx = cv2.cvtColor(mtx, cv2.COLOR_HSV2BGR)
    distance = (seg_error + class_error) / nb_hop

    algocog_time = time.time() - start_time
    print("Temps de calcul l'algorithme : %s secondes ---" % algocog_time)

    if WRITE_RESULTS:
        f_ac = open("../../results/algocog_computing.txt", "a")
        f_ac.write(str(algocog_time) + "\n")
        f_ac.close()
        name = audio_path.split('/')[-1]
        file = open("../results/error.txt", "a")
        file.write("\nERROR file " + name + ", " + str(hop_length) + ", " + str(nb_values) + ", " + str(teta) +
                   ", " + str(init) + "\nseg_error = " + str(seg_error) + "\nclass_error = " + str(class_error) +
                   "\ndistance = " + str(distance) + "\n")
        file.close()

    if SYNTHESIS == 1:
        name = audio_path.split('/')[-1][:-4] + '_synthesis.wav'
        print("name : ", name)
        class_s_mso.synthesis(ms_oracle, level, nb_hop, hop_length)

    if PLOT_ORACLE == 1:
        im = plot.start_draw(ms_oracle.levels[level].oracle, size=(900 * 4, 400 * 4))
        im.show()

    return 0