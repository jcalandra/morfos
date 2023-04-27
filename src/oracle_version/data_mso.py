import data_computing as dc
import similarity_functions as sf
import parameters as prm
import numpy as np
import cv2
import time
from mso import *
import synthesis_mso as s_mso
import algo_segmentation_mso as as_mso
import similarity_rules as sim_rules
import objects_storage as obj_s
import cost_storage as cs
import sys
import phases_storage as hs

# import compute_dynamics as cd

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

# COSTS
global gamma_t
cost_new_oracle = prm.cost_new_oracle

cost_numerisation = prm.cost_numerisation
cost_desc_computation = prm.cost_desc_computation
cost_seg_test_1 = prm.cost_seg_test_1

cost_new_mat_creation = prm.cost_new_mat_creation
cost_maj_autosim = prm.cost_maj_autosim
cost_maj_historique = prm.cost_maj_historique
cost_maj_df = prm.cost_maj_df
cost_print_df = prm.cost_print_df
cost_update = prm.cost_maj_concat_obj + prm.cost_maj_historique + prm.cost_maj_df # + prm.cost_polyphonie
cost_seg_test_2 = prm.cost_seg_test_2
cost_maj_concat_obj = prm.cost_maj_concat_obj
cost_test_EOS = prm.cost_test_EOS

cost_comparaison_2 = prm.cost_comparaison_2
cost_labelisation = prm.cost_labelisation
cost_maj_link = prm.cost_maj_link
cost_level_up = prm.cost_level_up


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


def build_oracle(flag, teta, nb_values, nb_hop, s_tab, v_tab):
    """Initialize an oracle with the given parameters."""
    volume_data = v_tab
    suffix_method = SUFFIX_METHOD

    if prm.processing == 'signal' and prm.MFCC_BIT == 1:
        dim = nb_values - 1
        input_data = s_tab.transpose()
    elif prm.processing == 'signal'and prm.FFT_BIT == 1 or prm.processing == 'vectors':
        dim = len(s_tab[0])
        input_data = np.array(s_tab)
    else:
        dim = nb_values
        input_data = s_tab.transpose()

    if type(input_data) != np.ndarray or type(input_data[0]) != np.ndarray:
        input_data = np.array(input_data)
    if input_data.ndim != 2:
        input_data = np.expand_dims(input_data, axis=1)

    oracle_t = oracle_mso.create_oracle(flag, threshold=teta, dfunc='cosine', dfunc_handle=None, dim=dim)

    return volume_data, suffix_method, input_data, oracle_t


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
        obj_s.first_occ_remove_obj(0)
        for i in range(len(matrix[1])):
            matrix[1][i].pop()
        actual_max = actual_max - 1
        temp_max = temp_max - 1
        mtx = np.delete(mtx, - 1, 0)
        return 1, matrix, actual_max, temp_max, mtx
    return 0, matrix, actual_max, temp_max, mtx


# ============================================ COGNITIVE ALGORITHM =====================================================
def prep_data(audio_path):
    """ Prepare the signal from continue to discrete values and add silence at the beginning."""
    here_time = time.time()
    data, rate, data_size, data_length = dc.get_data(audio_path)
    temps_data = time.time() - here_time
    if prm.verbose == 1:
        print("Temps data : %s secondes ---" % temps_data)

    nb_points = NB_SILENCE
    a = np.zeros(nb_points)
    data = np.concatenate((a, data))
    obj_s.data_init(data)
    return data, rate, data_size, data_length, nb_points


def matrix_init(data_length, nb_points=0, rate=1, data_size=0):
    """ Initialize the structure corresponding to the formal diagram of level 0."""
    # initialise matrix of each hop coordinates

    if prm.processing == 'signal':
        nb_sil_frames = nb_points / hop_length
        nb_hop = int(data_size / hop_length + nb_sil_frames) + 1
        data_length = data_length + nb_points / rate
        if data_size % hop_length < init:
            nb_hop = int(data_size / hop_length)
        if prm.verbose == 1:
            print("[RESULT] audio length = ", nb_hop)

    if prm.processing == 'vectors':
        nb_sil_frames = nb_points #TODO: modify the value eventually
        nb_hop = data_length + nb_sil_frames

    new_mat = np.ones((1, nb_hop, 3), np.uint8)
    for i in range(nb_hop):
        new_mat[0][i] = BACKGROUND
    mtx = new_mat.copy()
    obj_s.first_occ_add_level()
    obj_s.first_occ_add_obj(0, 0)
    return mtx, nb_hop, data_length


def algo_cog(path, oracles, end_mk=0):
    """ Compute the formal diagram of the audio at audio_path with threshold teta and size of frame hop_length."""

    # cost initialisations
    hs.phases_init()
    cs.cost_general_init()
    cs.cost_oracle_init()
    prm.time_tab = []
    prm.time_tab.append([])
    lambda_t = gamma_t = alpha_t = delta_t = beta_t = alpha_or_delta_t = new_mat = 0

    #
    if prm.verbose:
        print("[INFO] Computing the cognitive algorithm of the audio extract...")

    if prm.processing == 'signal':
        data, rate, data_size, data_length, nb_points = prep_data(path)
        if prm.COMPUTE_COSTS == 1:
            gamma_t += cost_numerisation
    elif prm.processing == 'vectors':
        #print(f"{path}")
        data = np.load(f"{path}", allow_pickle=True)
        if prm.to_transpose:
            data = data.T
        data_length = len(data)
        nb_points = 0
        rate = 1
        data_size = 0
    else:
        data, rate, data_size, data_length, nb_points = prep_data(path)
        if prm.COMPUTE_COSTS == 1:
            gamma_t += cost_numerisation

    mtx, nb_hop, data_length = matrix_init(data_length, nb_points, rate, data_size)

    if prm.verbose == 1:
        print("[INFO] Computing frequencies and volume...")
    if prm.processing == 'signal':
        nb_values = prm.NB_VALUES
        v_tab, s_tab = dc.get_descriptors(data, rate, hop_length, nb_hop, nb_values, init, fmin)
        if prm.COMPUTE_COSTS == 1:
            gamma_t += cost_desc_computation
    elif prm.processing == 'vectors':
        v_tab, s_tab = [(i % 4 + 0.9)/4 for i in range(data_length)], data
        nb_values = len(s_tab[0])
    else:
        nb_values = prm.NB_VALUES
        v_tab, s_tab = dc.get_descriptors(data, rate, hop_length, nb_hop, nb_values, init, fmin)
        if prm.COMPUTE_COSTS == 1:
            gamma_t += cost_desc_computation



    value = 255 - v_tab[0] * 255
    color = (BASIC_FRAME[0], BASIC_FRAME[1], value)
    mtx[0][0] = color

    seg_error = 0
    class_error = 0

    if prm.verbose == 1:
        print("[INFO] Structures initialisation...")

    # ------- CREATE AND BUILD VMO -------
    flag = 'a'
    volume_data, suffix_method, input_data, oracle_t = build_oracle(flag, teta, nb_values, nb_hop, s_tab, v_tab)
    if prm.COMPUTE_HYPOTHESIS:
        hs.phases_add_level()

    if prm.COMPUTE_COSTS == 1:
        cs.cost_general_add_level()
        cs.cost_oracle_add_level()
        lambda_t += cost_new_oracle
        prm.lambda_0 += lambda_t
        prm.lambda_levels[0].append(lambda_t)
        prm.lambda_sum[0].append(lambda_t)
        prm.lambda_tab.append(prm.lambda_0)
        prm.lambda_time.append(0)

    # ------- INITIALISATION OF OTHER STRUCTURES -------
    level = 0
    oracle_f, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix_next = \
        structure_init(flag, level, dim=nb_values)
    vec = [1]
    matrix = [chr(fd_mso.letter_diff + 1), [vec]]
    oracles[1].append(
        [oracle_t, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix_next, matrix])
    oracles[0] = level
    oracles[2] = data
    obj_s.objects_add_level()

    # ------- ALGORITHM -------
    prev_mat = prev2_mat = prev3_mat = 0
    actual_max = temp_max = 0
    color = color2 = (BASIC_FRAME[0], BASIC_FRAME[1], v_tab[0])
    diff_mk = 0

    if prm.verbose == 1:
        print("[INFO] Computing formal diagram...")

    prm.start_time_t = time.time()
    prm.max_time_t = 0
    # vsd, vdd, vkl, fsd, fdd = cd.compute_dynamics()
    for i_hop in range(nb_hop):  # while
        # CHECKPOINT #
        # Si le format fourni en entrée du logiciel est un fichier audio.
        # Vous trouvez ici l'information concernant l'avancement du calcul de l'algorithme (approximatif, ne prend pas
        # en compte certaines spécificités de comportement de l'algorithme possible aux niveaux supérieurs).
        # Envoi beaucoup d'information (autant que d'éléments au niveau 0), on peut donc choisir de filtrer seulement
        # certaines valeurs
        checkpoint = i_hop / nb_hop * 100
        if prm.checkpoint == 1:
            print("CHECKPOINT: ", checkpoint)
            sys.stdout.flush()
        # END CHECKPOINT #
        if len(matrix) != 0 and len(matrix[0]) > prm.NB_MAX_MATERIALS:
            sys.exit("You have reach more than " + str(prm.NB_MAX_MATERIALS) + " materials at level 0. Please lower your similarity threshold.")
        for i in range(1, len(oracles[1])):
            if len(oracles[1][i][2]) != 0 and len(oracles[1][i][2][0]) > prm.NB_MAX_MATERIALS:
                sys.exit("You have reach more than " + str(prm.NB_MAX_MATERIALS) + " at level " + str(i) + ". Please lower your similarity threshold.")

        if prm.verbose == 1:
            print("[INFO] Process in level 0...")

        obs = input_data[i_hop]
        oracle_t.add_state(obs, input_data, volume_data, suffix_method)
        if prm.COMPUTE_COSTS == 1:
            alpha_or_delta_t += prm.cost_total  # prm.cost_total or prm.cost_oracle_acq

        j_mat = oracle_t.data[i_hop + 1]
        value = 255 - v_tab[i_hop] * 255

        color3 = color2
        color2 = color
        color = (BASIC_FRAME[0], BASIC_FRAME[1], value)

        if i_hop > 0:
            prev_mat = oracle_t.data[i_hop]
        if i_hop > 1:
            prev2_mat = oracle_t.data[i_hop - 1]
        if i_hop > 2:
            prev3_mat = oracle_t.data[i_hop - 2]

        if i_hop == nb_hop - 1 and j_mat != prev_mat:
            modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data)
            j_mat = prev_mat
        if prm.COMPUTE_COSTS:
            alpha_or_delta_t += cost_seg_test_1

        if prm.processing == 'signal':
            diff = sf.dissimilarity(i_hop, s_tab, v_tab)
        elif prm.processing == 'vectors':
            diff = 0
            actual_char = j_mat + 1
            actual_char_ind = i_hop + 1
            k = 0
            level_max = oracles[0]
            str_obj = None
            test_1, test_2, test_3, test_4, test_5a, test_5b, test_6a, test_6b, test_7a, test_7b, test_8a, test_8b, \
            i_hop, k, actual_char, oracle_t, link, history_next, concat_obj, \
            formal_diagram, formal_diagram_graph, str_obj, input_data = sim_rules.rules_parametrization(
                oracle_t, matrix, actual_char, actual_char_ind, link, oracles, level, i_hop, k, history_next, concat_obj,
                formal_diagram, formal_diagram_graph, str_obj, input_data, level_max, end_mk)
            if ((test_1 and test_2) or (test_2 and test_3) or test_4 or test_6b or test_7b or test_8b) \
                    and (test_5a and test_5b and test_6a and test_7a and test_8a):
                j_mat = actual_char - 1
                diff = 1
        else:
            diff = sf.dissimilarity(i_hop, s_tab, v_tab)

        if diff and ((prm.processing == 'signal' and len(concat_obj) > 3) or prm.processing == 'vectors'):
            if diff_mk != 1:
                if SEGMENTATION_BIT:
                    color = SEGMENTATION

                if i_hop == nb_hop - 1:
                    end_mk = 1
                    concat_obj = concat_obj + chr(fd_mso.letter_diff + oracle_t.data[i_hop + 1] + 1)
                # link update
                if len(oracles[1]) > level + 1:
                    # node = len(oracles[1][level + 1][0].data)
                    node = max(oracles[1][level][1]) + 1
                else:
                    node = 1
                for ind in range(len(concat_obj)):
                    link.append(node)
                # history_next update
                new_char = sim_rules.char_next_level_similarity(oracles, level)
                # concat_obj update
                concat_obj = ""

                diff_mk = 1
                as_mso.fun_segmentation(oracles, new_char, nb_hop, level=level + 1, end_mk=end_mk)
                if prm.verbose == 1:
                    print("[INFO] Process in level 0...")
        else:
            diff_mk = 0
            if i_hop == nb_hop - 1:
                end_mk = 1
                concat_obj = concat_obj + chr(fd_mso.letter_diff + oracle_t.data[i_hop + 1] + 1)
                # link update
                if len(oracles[1]) > level + 1:
                    node = max(oracles[1][level][1]) + 1
                else:
                    node = 1
                for ind in range(len(concat_obj)):
                    link.append(node)
                # history_next update
                new_char = sim_rules.char_next_level_similarity(oracles, level)
                # concat_obj update
                concat_obj = ""
                diff_mk = 1
                as_mso.fun_segmentation(oracles, new_char, nb_hop, level=level + 1, end_mk=end_mk)
                if prm.verbose == 1:
                    print("[INFO] Process in level 0...")

        if j_mat > actual_max:

            if i_hop > 2 and prev_mat != prev2_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                seg_error = seg_error + 1
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 2, j_mat, prev2_mat, s_tab)
                if good_mat == j_mat:
                    modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data)
                    j_mat = oracle_t.data[i_hop]

                else:
                    modify_oracle(oracle_t, prev2_mat, prev_mat, i_hop - 1, input_data)
                    digit, matrix, actual_max, temp_max, mtx = \
                        modify_matrix(mtx, prev_mat, matrix, actual_max, temp_max, i_hop - 1)
                    if digit == 1:
                        j_mat -= 1

            elif i_hop > 2 and prev_mat != prev3_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = SEG_ERROR
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 3, j_mat, prev3_mat, s_tab)
                if good_mat == j_mat:
                    modify_oracle(oracle_t, prev_mat, j_mat, i_hop, input_data)
                    j_mat = oracle_t.data[i_hop]
                    temp_max = j_mat
                else:
                    modify2_oracle(oracle_t, prev3_mat, prev2_mat, prev_mat, i_hop - 1, input_data)
                    digit, matrix, actual_max, temp_max, mtx = \
                        modify_matrix(mtx, prev_mat, matrix, actual_max, temp_max, i_hop - 1)
                    if digit == 1:
                        j_mat -= 1
                    digit, matrix, actual_max, temp_max, mtx = \
                        modify_matrix(mtx, prev2_mat, matrix, actual_max, temp_max, i_hop - 2)
                    if digit == 1:
                        j_mat -= 1
                    seg_error = seg_error + 2

        if j_mat > actual_max:
            temp_max = j_mat
            new_mat = 1
            if prm.COMPUTE_COSTS:
                alpha_t += cost_maj_autosim + cost_maj_df
            vec = oracle_t.vec[len(matrix[0]) - 1].copy()
            vec.append(1)
            matrix[0] += (chr(len(matrix[0]) + fd_mso.letter_diff + 1))
            matrix[1].append(vec)
            for i in range(len(matrix[1]) - 1):
                matrix[1][i].append(matrix[1][len(matrix[1]) - 1][i])
            new_mat_l = np.ones((1, nb_hop, 3), np.uint8)
            for i in range(nb_hop):
                new_mat_l[0][i] = BACKGROUND
            mtx = np.concatenate((mtx, new_mat_l))
            first_occ_mat = i_hop*(prm.HOP_LENGTH/prm.SR)
            obj_s.first_occ_add_obj(level, first_occ_mat)

        else:

            if i_hop > 2 and prev_mat != prev2_mat and j_mat != prev_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 1
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 2, j_mat, prev2_mat, s_tab)

                # By default the best element is the previous one because FO cannot point on future objects
                modify_oracle(oracle_t, good_mat, prev_mat, i_hop - 1, input_data)
                digit, matrix, actual_max, temp_max, mtx = \
                    modify_matrix(mtx, prev_mat, matrix, actual_max, temp_max, i_hop - 1)

            if i_hop > 2 and prev_mat == prev2_mat and prev_mat != prev3_mat and j_mat != prev_mat and CORRECTION_BIT:
                if CORRECTION_BIT_COLOR:
                    color = CLASS_ERROR
                class_error = class_error + 2
                good_mat = sf.true_mat(i_hop - 1, i_hop, i_hop - 3, j_mat, prev3_mat, s_tab)
                modify2_oracle(oracle_t, good_mat, prev2_mat, prev_mat, i_hop - 1, input_data)
                digit, matrix, actual_max, temp_max, mtx = \
                    modify_matrix(mtx, prev_mat, matrix, actual_max, temp_max, i_hop - 1)
                digit, matrix, actual_max, temp_max, mtx = \
                    modify_matrix(mtx, prev2_mat, matrix, actual_max, temp_max, i_hop - 2)

        if i_hop > 0:
            for k in range(len(mtx)):
                mtx[k][len(oracle_t.data) - 2] = BACKGROUND
            mtx[oracle_t.data[i_hop + 1]][i_hop] = color
            if i_hop > 1:
                for k in range(len(mtx)):
                    mtx[k][len(oracle_t.data) - 3] = BACKGROUND
                mtx[oracle_t.data[i_hop]][i_hop - 1] = color2
            if i_hop > 2:
                for k in range(len(mtx)):
                    mtx[k][len(oracle_t.data) - 4] = BACKGROUND
                mtx[oracle_t.data[i_hop - 1]][i_hop - 2] = color3
            if prm.POLYPHONY:
                if i_hop > 1:
                    for mat in range(1, oracle_t.data[i_hop - 1]):
                        value = min((1 - matrix[1][oracle_t.data[i_hop - 1]][mat]) / (1 - prm.min_matrix) * 255, 255)
                        mtx[mat][i_hop - 2] = (BASIC_FRAME[0], BASIC_FRAME[1], value)
                if i_hop > 0:
                    for mat in range(1, oracle_t.data[i_hop]):
                        value = min((1 - matrix[1][oracle_t.data[i_hop]][mat]) / (1 - prm.min_matrix) * 255, 255)
                        mtx[mat][i_hop - 1] = (BASIC_FRAME[0], BASIC_FRAME[1], value)
                for mat in range(1, oracle_t.data[i_hop + 1]):
                    value = min((1 - matrix[1][oracle_t.data[i_hop + 1]][mat]) / (1 - prm.min_matrix) * 255, 255)
                    mtx[mat][i_hop] = (BASIC_FRAME[0], BASIC_FRAME[1], value)

        if len(concat_obj) == 1:
            if len(history_next) > 0:
                new_history_next_element = history_next[-1][1]
                if ord(history_next[-1][1][-2]) - fd_mso.letter_diff > len(matrix[0]):
                    tmp_char = history_next[-1][1][-1]
                    new_history_next_element = new_history_next_element[:-2]
                    new_history_next_element += chr(oracle_t.data[i_hop - 1] + fd_mso.letter_diff + 1)
                    new_history_next_element += tmp_char
                if ord(history_next[-1][1][-1]) - fd_mso.letter_diff > len(matrix[0]):
                    new_history_next_element = new_history_next_element[:-1]
                    new_history_next_element += chr(oracle_t.data[i_hop - 1] + fd_mso.letter_diff + 1)
                history_next[-1] = (history_next[-1][0], new_history_next_element, history_next[-1][2])
            concat_obj = chr(fd_mso.letter_diff + oracle_t.data[i_hop] + 1)

        if len(concat_obj) == 2:
            if len(history_next) > 0:
                new_history_next_element = history_next[-1][1]
                if ord(history_next[-1][1][-1]) - fd_mso.letter_diff > len(matrix[0]):
                    new_history_next_element = new_history_next_element[:-1]
                    new_history_next_element += chr(oracle_t.data[i_hop - 1] + fd_mso.letter_diff + 1)
                history_next[-1] = (history_next[-1][0], new_history_next_element, history_next[-1][2])
            concat_obj = chr(fd_mso.letter_diff + oracle_t.data[i_hop - 1] + 1) + \
                         chr(fd_mso.letter_diff + oracle_t.data[i_hop] + 1)
            # TODO: corriger la valeur dans la matrice

        if len(concat_obj) >= 3:
            concat_obj = concat_obj[:len(concat_obj) - 2] + chr(fd_mso.letter_diff + oracle_t.data[i_hop - 1] + 1) \
                         + chr(fd_mso.letter_diff + oracle_t.data[i_hop] + 1)
        concat_obj = concat_obj + chr(fd_mso.letter_diff + oracle_t.data[i_hop + 1] + 1)

        if temp_max > actual_max:
            actual_max = temp_max
        formal_diagram = cv2.cvtColor(mtx, cv2.COLOR_HSV2BGR)
        fd_mso.print_formal_diagram_update(formal_diagram_graph, level, formal_diagram, nb_hop)
        if prm.COMPUTE_COSTS:
            alpha_or_delta_t += cost_update + cost_print_df

        oracles[1][level][0] = oracle_t
        oracles[1][level][1] = link
        oracles[1][level][2] = history_next
        oracles[1][level][3] = concat_obj
        oracles[1][level][4] = formal_diagram
        oracles[1][level][5] = formal_diagram_graph

        links = []
        if prm.processing == 'signal':
            sound = obj_s.data[i_hop*prm.HOP_LENGTH:(i_hop + 1)*prm.HOP_LENGTH]
        elif prm.processing == 'vectors':
            sound = [0]
        else:
            sound = obj_s.data[i_hop*prm.HOP_LENGTH:(i_hop + 1)*prm.HOP_LENGTH]
        id = i_hop
        mat_num = oracle_t.data[i_hop + 1]
        x = (prm.HOP_LENGTH/prm.SR)*(i_hop + 1)
        y = obj_s.first_occ[level][mat_num]
        z = prm.HOP_LENGTH/prm.SR
        obj_s.objects_add_new_obj(id, links, x, y, z, mat_num, level, sound)

        if prm.COMPUTE_HYPOTHESIS or prm.COMPUTE_COSTS:
            if prm.TIME_TYPE == prm.STATE_TIME:
                time_t = obj_s.objects[level][len(obj_s.objects[level]) - 1]["coordinates"]["x"]
            elif prm.TIME_TYPE == prm.COMPUTING_TIME:
                prm.real_time_t = time.time() - prm.start_time_t
                time_t = prm.real_time_t
            elif prm.TIME_TYPE == prm.MAX_TIME:
                prm.max_time_t = max(obj_s.objects[level][len(obj_s.objects[level]) - 1]["coordinates"]["x"],
                                 prm.max_time_t)
                time_t = prm.max_time_t
            else:
                prm.max_time_t = max(obj_s.objects[level][len(obj_s.objects[level]) - 1]["coordinates"]["x"],
                                     prm.max_time_t)
                time_t = prm.max_time_t
            if len(prm.time_tab[level]) > 0:
                prev_time_t =  prm.time_tab[level][len(prm.time_tab[level]) - 1]
            else:
                prev_time_t = None
            prm.time_tab[level].append(time_t)

        if prm.COMPUTE_COSTS == 1:
            if prm.verbose:
                print("gamma_", i_hop, " level ", level, ": ", gamma_t)
            prm.gamma += gamma_t

            if new_mat:
                delta_t = 0
                alpha_t += alpha_or_delta_t
            else:
                alpha_t = 0
                delta_t += alpha_or_delta_t
            if delta_t > 0:
                if prm.verbose:
                    print("delta_", i_hop, " level ", level, ": ", delta_t)
                prm.delta += delta_t
                prm.delta_tab.append(prm.delta)
                prm.delta_time.append(time_t)

            if alpha_t > 0:
                if prm.verbose:
                    print("alpha_", i_hop, " level ", level, ": ", alpha_t)
                prm.alpha += alpha_t
                prm.alpha_tab.append(prm.alpha)
                prm.alpha_time.append(time_t)

            if lambda_t == 0:
                prm.lambda_levels[level].append(lambda_t)
                if len(prm.lambda_sum[level]) >= 1:
                    prm.lambda_sum[level].append(prm.lambda_sum[level][-1] + lambda_t)
                else:
                    prm.lambda_sum[level].append(lambda_t)
            if lambda_t != 0:
                lambda_t = 0
            prm.gamma_levels[level].append(gamma_t)
            prm.alpha_levels[level].append(alpha_t)
            prm.beta_levels[level].append(beta_t)
            prm.delta_levels[level].append(delta_t)

            if len(prm.gamma_sum[level]) >= 1:
                prm.gamma_sum[level].append(prm.gamma_sum[level][-1] + gamma_t)
                prm.alpha_sum[level].append(prm.alpha_sum[level][-1] + alpha_t)
                prm.beta_sum[level].append(prm.beta_sum[level][-1] + beta_t)
                prm.delta_sum[level].append(prm.delta_sum[level][-1] + delta_t)
            else:
                prm.gamma_sum[level].append(gamma_t)
                prm.alpha_sum[level].append(alpha_t)
                prm.beta_sum[level].append(beta_t)
                prm.delta_sum[level].append(delta_t)
            prm.gamma_tab.append(prm.gamma)
            prm.gamma_time.append(time_t)

            cs.cost_oracle_add_element(level, time_t)
            gamma_t = cost_numerisation + cost_desc_computation
            prev_nmat = new_mat
            alpha_t = beta_t = delta_t = alpha_or_delta_t = new_mat = 0

        if prm.COMPUTE_COSTS:
            if len(prm.alpha_levels[level]) > 1:
                prev_cost = prm.alpha_levels[level][-2] + \
                            prm.beta_levels[level][-2] + \
                            prm.lambda_levels[level][-2] + \
                            prm.delta_levels[level][-2]
            else:
                prev_cost = 0
            cost = alpha_t + beta_t + lambda_t + delta_t

        if prm.COMPUTE_HYPOTHESIS:
            if i_hop > 0:
                hs.phases_add_element(level, prev_nmat, diff, prev_time_t, prev_cost)
            if i_hop == nb_hop - 1:
                hs.phases_add_element(level, new_mat, 1, time_t, cost)

        if i_hop > 3:
            mat_num_prev1 = oracle_t.data[i_hop]
            mat_num_prev2 = oracle_t.data[i_hop - 1]
            y_prev1 = obj_s.first_occ[level][mat_num_prev1]
            y_prev2 = obj_s.first_occ[level][mat_num_prev2]
            obj_s.objects_modify_prev_obj(level, mat_num_prev1, mat_num_prev2, y_prev1, y_prev2)

    if prm.COMPUTE_COSTS == 1:
        prm.lambda_tab.append(prm.lambda_0)
        prm.lambda_time.append(time_t)
    if flag != 'f' and flag != 'v':
        oracle_t.f_array.finalize()

    mtx = cv2.cvtColor(mtx, cv2.COLOR_HSV2BGR)
    distance = (seg_error + class_error) / nb_hop

    algocog_time = time.time() - prm.start_time_t
    if prm.SHOW_TIME:
        print("Temps de calcul l'algorithme : %s secondes ---" % algocog_time)

    if WRITE_RESULTS:
        f_ac = open("../../results/algocog_computing.txt", "a")
        f_ac.write(str(algocog_time) + "\n")
        f_ac.close()
        name = path.split('/')[-1]
        file = open("../results/error.txt", "a")
        file.write("\nERROR file " + name + ", " + str(hop_length) + ", " + str(nb_values) + ", " + str(teta) +
                   ", " + str(init) + "\nseg_error = " + str(seg_error) + "\nclass_error = " + str(class_error) +
                   "\ndistance = " + str(distance) + "\n")
        file.close()

    if SYNTHESIS == 1:
        name = path.split('/')[-1][:-4] + '_synthesis.wav'
        print("name : ", name)
        s_mso.synthesis(oracle_t, nb_hop, data, hop_length, rate, name)

    return mtx, data_length, data_size, distance, algocog_time
