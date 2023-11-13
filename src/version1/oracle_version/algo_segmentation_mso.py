import sys
import time
import mso
import version1.parameters as prm
import formal_diagram_mso as fd_mso
import similarity_rules
import objects_storage as obj_s
import cost_storage as cs
import phases_storage as hs

# In this file is defined the main loop for the algorithm at symbolic scale
# structring test function according to rules (rules_parametrization) and similarity test function
# (char_next_level_similarity) are also defined here

letter_diff = prm.LETTER_DIFF
wait = 0
processing = prm.processing

# COSTS


cost_new_oracle = prm.cost_new_oracle

cost_numerisation = prm.cost_numerisation
cost_desc_computation = prm.cost_desc_computation
cost_seg_test_1 = prm.cost_seg_test_1

cost_new_mat_creation = prm.cost_new_mat_creation
cost_maj_autosim = prm.cost_maj_autosim
cost_maj_historique = prm.cost_maj_historique
cost_maj_df = prm.cost_maj_df
cost_print_df = prm.cost_print_df
cost_seg_test_2 = prm.cost_seg_test_2
cost_maj_concat_obj = prm.cost_maj_concat_obj
cost_test_EOS = prm.cost_test_EOS

cost_comparaison_2 = prm.cost_comparaison_2
cost_labelisation = prm.cost_labelisation
cost_maj_link = prm.cost_maj_link
cost_level_up = prm.cost_level_up


# ============================================ SEGMENTATION FUNCTION ===================================================
def structure(concat_obj, oracles, level, link, data_length, level_max, end_mk):
    """ Function for the structuring operation and therfore the update of the structures at this level and next level"""
    # Labelling upper level string and updating the different structures
    new_char = similarity_rules.char_next_level_similarity(oracles, level)
    if len(oracles[1]) > level + 1:
        node = max(oracles[1][level][1]) + 1
    else:
        node = 1
    for ind in range(len(concat_obj)):
        link.append(node)

    # send to the next f_oracle the node corresponding to concat_obj
    fun_segmentation(oracles, new_char, data_length, level + 1, level_max, end_mk)
    return 0


# ================================= MAIN COGNITIVE ALGORITHM AT SYMBOLIC SCALE =========================================
def fun_segmentation(oracles, str_obj, data_length, level=0, level_max=-1, end_mk=0):
    """This function browses the string char and structure it at the upper level according to the rules that are applied
    by the extern user."""
    # end of the recursive loop
    if level > oracles[0] and end_mk == 1:
        return 0

    #  Initialisation of the structures
    if level > oracles[0]:
        if prm.COMPUTE_COSTS and level == 0:
            hs.phases_init()
            cs.cost_general_init()
            cs.cost_oracle_init()

        if prm.verbose == 1:
            print("[INFO] CREATION OF NEW FO : LEVEL " + str(level) + "...")
        flag = 'f'

        f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, matrix_next = \
            mso.structure_init(flag, level)
        matrix = [chr(fd_mso.letter_diff + ord(str_obj[0])), [[1]]]

        oracles[0] = level
        level_max = level

        if level == 0 and processing == 'symbols':
            for i in range(len(oracles[1])):
                if len(oracles[1][i][2][0]) > prm.NB_MAX_MATERIALS:
                    sys.exit("You have reach more than " + str(prm.NB_MAX_MATERIALS) + " materials at level " + str(i) + ". Please lower your similarity threshold.")
            prm.start_time_t = time.time()
            prm.max_time_t = 0
            prm.time_tab = []
            prm.time_tab.append([])
            vec = [1]
            matrix = [chr(ord(str_obj[0])), [vec]]
            oracles[1].append([f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph,
                               matrix_next, matrix])
        elif level > 0:
            prm.time_tab.append([])
            matrix = oracles[1][level - 1][6]
            oracles[1].append([f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph,
                               matrix_next])

        if prm.COMPUTE_COSTS:
            if level == 0:
                time_t = 0
            else:
                if prm.TIME_TYPE == prm.STATE_TIME:
                    time_t = obj_s.objects[level - 1][len(obj_s.objects[level - 1]) - 1]["coordinates"]["x"]
                elif prm.TIME_TYPE == prm.COMPUTING_TIME:
                    prm.real_time_t = time.time() - prm.start_time_t
                    time_t = prm.real_time_t
                elif prm.TIME_TYPE == prm.MAX_TIME:
                    prm.max_time_t = max(obj_s.objects[level - 1][len(obj_s.objects[level - 1]) - 1]
                                         ["coordinates"]["x"], prm.max_time_t)
                    time_t = prm.max_time_t
                else:
                    prm.max_time_t = max(obj_s.objects[level - 1][len(obj_s.objects[level - 1]) - 1]
                                         ["coordinates"]["x"], prm.max_time_t)
                    time_t = prm.max_time_t
            hs.phases_add_level()
            cs.cost_general_add_level()
            cs.cost_oracle_add_level()
            lambda_t = cost_new_oracle
            prm.lambda_0 += lambda_t
            prm.lambda_levels[level].append(lambda_t)
            prm.lambda_sum[level].append(lambda_t)
            prm.lambda_tab.append(prm.lambda_0)
            prm.lambda_time.append(time_t)

    else:
        f_oracle = oracles[1][level][0]
        link = oracles[1][level][1]
        history_next = oracles[1][level][2]
        concat_obj = oracles[1][level][3]
        formal_diagram = oracles[1][level][4]
        formal_diagram_graph = oracles[1][level][5]
        if level > 0:
            matrix = oracles[1][level - 1][6]
        else:
            matrix = oracles[1][level][7]

    # Every new character is analysed.
    input_data = [ord(str_obj[ind_input]) - letter_diff for ind_input in range(len(str_obj))]
    level_wait = -1
    global wait
    k = len(f_oracle.data) - 1
    i = 0
    if prm.verbose == 1:
        print("[INFO] Process in level " + str(level) + "...")
    while i < len(str_obj):
        # CHECKPOINT #
        # Si le format fournit en entrée du logiciel est une chaîne de caractères.
        # Vous trouvez ici l'information concernant l'avancement du calcul de l'algorithme (approximatif, ne prend pas
        # en compte certaines spécificités de comportement de l'algorithme possible aux niveaux supérieurs).
        # Envoi beaucoup d'information (autant que d'éléments au niveau 0), on peut donc choisir de filtrer seulement
        # certaines valeurs
        if level == 0 and processing == 'symbols':
            checkpoint = (k + i)/(k + len(str_obj))*100
            if prm.checkpoint == 1:
                print("CHECKPOINT: ", checkpoint)
                sys.stdout.flush()
        # END CHECKPOINT #
        f_oracle.add_state(input_data[i])
        actual_char = f_oracle.data[k + i + 1]  # i_th parsed character
        actual_char_ind = k + i + 1
        # if there is only one object in this class of material, it's a new material
        diff = 0
        if len(f_oracle.latent[f_oracle.data[k + i + 1] - 1]) == 1:
            new_mat = 1
        else:
            new_mat = 0
        if i + k > 0 and (len(f_oracle.latent[f_oracle.data[k + i] - 1]) == 1
                or (f_oracle.data[k + i] == f_oracle.data[k + i + 1]
                    and len(f_oracle.latent[f_oracle.data[k + i] - 1]) == 2)):
            prev_nmat = 1
        else:
            prev_nmat = 0

        if level == 0 and processing == 'symbols' and \
                actual_char > max([ord(matrix[0][ind]) - letter_diff for ind in range(len(matrix[0]))]):
            vec = [0 for ind_vec in range(len(matrix[0]))]
            vec.append(1)
            matrix[0] += chr(actual_char + letter_diff)
            matrix[1].append(vec)
            for ind_mat in range(len(matrix[1]) - 1):
                matrix[1][ind_mat].append(matrix[1][len(matrix[1]) - 1][ind_mat])

        # formal diagram is updated with the new char
        if actual_char_ind == 1:
            fd_mso.formal_diagram_init(formal_diagram, data_length, oracles, level)
        else:
            fd_mso.formal_diagram_update(formal_diagram, data_length, actual_char, actual_char_ind, oracles, level)

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
        lambda_t = gamma_t = beta_t = alpha_t = delta_t = alpha_or_delta_t = 0
        if len(prm.time_tab[level]) > 0:
            prev_time_t =  prm.time_tab[level][len(prm.time_tab[level]) - 1]
        else:
            prev_time_t = None
        prm.time_tab[level].append(time_t)

        if prm.COMPUTE_COSTS == 1:
            cs.cost_oracle_add_element(level, time_t)
            alpha_or_delta_t = prm.cost_total  # prm.cost_total or prm.cost_oracle_acq
            if new_mat:
                alpha_t = cost_maj_df + cost_maj_historique + cost_maj_autosim #TODO: à mettre dans alpha_or_delta_t et faire une variable qui dépend de nouveau mat ou non
                delta_t = 0
            else:
                alpha_t = 0
                delta_t = 0

            if i == 0 and level > 0:
                beta_t = cost_comparaison_2 + cost_labelisation + cost_maj_link + cost_level_up
                if prm.verbose:
                    print("beta_", actual_char_ind - 1, " level ", level, ": ", beta_t)
                prm.beta += beta_t
                prm.beta_tab.append(prm.beta)
                prm.beta_time.append(time_t)

            alpha_or_delta_t += cost_print_df

        oracles[1][level][5] = fd_mso.print_formal_diagram_update(
            formal_diagram_graph, level, formal_diagram, data_length)

        # First is the parametrisation of the rules according to the external settings.
        test_1, test_2, test_3, test_4, test_5, test_6a, test_6b, test_7a, test_7b, test_8a, test_8b, \
        i, k, actual_char, f_oracle, link, history_next, concat_obj, \
        formal_diagram, formal_diagram_graph, str_obj, input_data = similarity_rules.rules_parametrization(
                f_oracle, matrix, actual_char, actual_char_ind, link, oracles, level, i, k, history_next, concat_obj,
                formal_diagram, formal_diagram_graph, str_obj, input_data, level_max, end_mk)

        if level > 0 and end_mk == 1 and i < len(str_obj) - 1:
            end_mk = 0
            wait = 1
            level_wait = level

        # If the tests are positives, there is structuration.
        if prm.COMPUTE_COSTS == 1:
            alpha_or_delta_t += cost_seg_test_2
        if ((test_1 and test_2) or (test_2 and test_3) or test_4 or test_6b or test_7b or test_8b) \
                and (test_5 and test_6a and test_7a and test_8a) and (end_mk == 0):
            diff = 1
            # or (end_mk == 1 and len(concat_obj) != 0):
            if prm.verbose == 1:
                print("[INFO] structure in level " + str(level) + "...")
            structure(concat_obj, oracles, level, link, data_length, level_max, end_mk)
            if prm.verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            concat_obj = ''
        concat_obj = concat_obj + chr(actual_char + letter_diff)

        if prm.COMPUTE_COSTS == 1:
            alpha_or_delta_t += cost_maj_concat_obj
        oracles[1][level][3] = concat_obj

        if prm.COMPUTE_COSTS == 1:
            alpha_or_delta_t += cost_test_EOS
            if new_mat:
                delta_t = 0
                alpha_t += alpha_or_delta_t
            else:
                alpha_t = 0
                delta_t += alpha_or_delta_t
            if delta_t > 0:
                if prm.verbose:
                    print("delta_", actual_char_ind - 1, " level ", level, ": ", delta_t)
                prm.delta += delta_t
                prm.delta_tab.append(prm.delta)
                prm.delta_time.append(time_t)

            if alpha_t > 0:
                if prm.verbose:
                    print("alpha_", actual_char_ind - 1, " level ", level, ": ", alpha_t)
                prm.alpha += alpha_t
                prm.alpha_tab.append(prm.alpha)
                prm.alpha_time.append(time_t)

            if actual_char_ind > 1:
                prm.lambda_levels[level].append(lambda_t)
            prm.beta_levels[level].append(beta_t)
            prm.alpha_levels[level].append(alpha_t)
            prm.delta_levels[level].append(delta_t)
            prm.gamma_levels[level].append(gamma_t)
            if actual_char_ind != 1:
                prm.lambda_sum[level].append(prm.lambda_sum[level][-1] + lambda_t)
            if len(prm.beta_sum[level]) >= 1:
                prm.gamma_sum[level].append(prm.gamma_sum[level][-1] + gamma_t)
                prm.beta_sum[level].append(prm.beta_sum[level][-1] + beta_t)
                prm.alpha_sum[level].append(prm.alpha_sum[level][-1] + alpha_t)
                prm.delta_sum[level].append(prm.delta_sum[level][-1] + delta_t)
            else:
                prm.gamma_sum[level].append(gamma_t)
                prm.beta_sum[level].append(beta_t)
                prm.alpha_sum[level].append(alpha_t)
                prm.delta_sum[level].append(delta_t)

        if prm.COMPUTE_HYPOTHESIS:
            if len(prm.alpha_levels[level]) > 1:
                prev_cost = prm.alpha_levels[level][-2] + \
                            prm.beta_levels[level][-2] + \
                            prm.lambda_levels[level][-2] + \
                            prm.delta_levels[level][-2]
            else:
                prev_cost = 0
            cost = alpha_t + beta_t + lambda_t + delta_t
            if i + k > 0:
                hs.phases_add_element(level, prev_nmat, diff, prev_time_t, prev_cost)
                prev_cost = cost

        # Automatically structuring if this is the End Of String
        if (level == 0 and i == len(str_obj) - 1) or (wait == 1 and level == level_wait and i == len(str_obj) - 1):
            end_mk = 1
            wait = 0
            level_wait = -1
            if prm.COMPUTE_HYPOTHESIS:
                if i + k > 0:
                    hs.phases_pop_element(level)

        if end_mk == 1:
            if diff == 0:
                diff = 1
            else:
                diff = 0
            structure(concat_obj, oracles, level, link, data_length, level_max, end_mk)
            if prm.COMPUTE_HYPOTHESIS:
                # TODO: fix bug at level 0
                if i + k > 0:
                    hs.phases_add_element(level, new_mat, diff, time_t, cost)
            if prm.verbose == 1:
                print("[INFO] Process in level " + str(level) + "...")
            concat_obj = ''
        oracles[1][level][3] = concat_obj
        i += 1
        if prm.verbose == 1:
            print("state number ", i, " in level ", level)

    return 1