import similarity_computation
import segmentation_rules_mso
import formal_diagram_mso as fd_mso
from raw_implementation.parameters import LETTER_DIFF, STRICT_EQUALITY, ALIGNMENT, processing
letter_diff = LETTER_DIFF


def rules_parametrization(f_oracle, matrix, actual_char, actual_char_ind, link, oracles, level, i, k, history_next,
                          concat_obj, formal_diagram, formal_diagram_graph, str_obj, input_data, level_max, end_mk):
    """ Structuring test function: if one test is validated, there is structuration."""
    potential_obj = None
    if segmentation_rules_mso.RULE_1a:
        # test_1 = segmentation_rules_mso.rule_1a_similarity_mat(f_oracle, actual_char_ind)
        test_1 = segmentation_rules_mso.rule_1b_similarity_word(oracles, level, actual_char)
    else:
        test_1 = 1
    if segmentation_rules_mso.RULE_2:
        test_2 = segmentation_rules_mso.rule_2_not_validated_hypothesis(f_oracle, link, actual_char, actual_char_ind)
    else:
        test_2 = 1
    if not segmentation_rules_mso.RULE_1a and not segmentation_rules_mso.RULE_2:
        test_1 = 0
        test_2 = 0
    if segmentation_rules_mso.RULE_4:
        test_4, potential_obj = segmentation_rules_mso.rule_4_recomputed_object(
            oracles, matrix, level, actual_char_ind, str_obj, k, level_max, end_mk)
    else:
        test_4 = 0
    if segmentation_rules_mso.RULE_3 and test_4 == 0:
        test_3 = segmentation_rules_mso.rule_3_existing_object(history_next, concat_obj, actual_char, matrix)
    else:
        test_3 = 0
    if segmentation_rules_mso.RULE_5a:
        test_5a = segmentation_rules_mso.rule_5a_regathering_after(concat_obj)
    else:
        test_5a = 1
    if segmentation_rules_mso.RULE_5b:
        test_5a = 1
        test_5b = segmentation_rules_mso.rule_5b_regathering_before()
    else:
        test_5b = 1
    if segmentation_rules_mso.RULE_6:
        test_5a = 1
        test_5b = 1
        test_6a = segmentation_rules_mso.rule_6a_low_bound(concat_obj)
        test_6b = segmentation_rules_mso.rule_6b_high_bound(concat_obj)
    else:
        test_6a = 1
        test_6b = 0
    if segmentation_rules_mso.RULE_7:
        test_5a = 1
        test_5b = 1
        test_6a = 1
        test_6b = 0
        test_7a = segmentation_rules_mso.rule_7a_mean_word_length_low(f_oracle, concat_obj)
        test_7b = segmentation_rules_mso.rule_7b_mean_word_length_high(f_oracle, concat_obj)
    else:
        test_7a = 1
        test_7b = 0
    if segmentation_rules_mso.RULE_8:
        test_8a = segmentation_rules_mso.rule_8a_repetition_paradigm_noseg(f_oracle, actual_char_ind, concat_obj)
        test_8b = segmentation_rules_mso.rule_8b_repetition_paradigm_seg(f_oracle, actual_char_ind, concat_obj)
        if test_6b or test_7b:
            test_8a = 1
    else:
        test_8a = 1
        test_8b = 0

    if processing != 'vectors' and test_4:
        f_oracle = oracles[1][level][0]
        link = oracles[1][level][1]
        history_next = oracles[1][level][2]
        concat_obj = oracles[1][level][3]
        formal_diagram = oracles[1][level][4]

        str_obj = potential_obj
        input_data = [ord(potential_obj[i]) - letter_diff for i in range(len(potential_obj))]

        i = len(concat_obj)
        k = len(f_oracle.data) - len(concat_obj) - 1
        f_oracle.add_state(input_data[i])
        actual_char = f_oracle.data[k + i + 1]
        data_length = len(formal_diagram[0])
        fd_mso.formal_diagram_update(formal_diagram, data_length, actual_char, k + i + 1, oracles, level)
        oracles[1][level][5] = fd_mso.print_formal_diagram_update(
            formal_diagram_graph, level, formal_diagram, data_length)
        formal_diagram_graph = oracles[1][level][5]

    return test_1, test_2, test_3, test_4, test_5a, test_5b, test_6a, test_6b, test_7a, test_7b, test_8a, test_8b, \
           i, k, actual_char, \
           f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph, str_obj, input_data

# ================================================ SIMILARITY ==========================================================
def similarity_strict(oracles, level):
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    sim_tab = [0 for ind in range(len(history_next))]
    for i in range(len(history_next)):
        if len(concat_obj) == len(history_next[i][1]):
            j = 0
            while history_next[i][1][j] == concat_obj[j]:
                j = j + 1
                if j == len(history_next[i][1]):
                    new_char = history_next[i][0]
                    return new_char, None, sim_tab, 1
    return None, None, sim_tab, 0


def similarity_alignment(oracles, level):
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    if level > 0:
        matrix = oracles[1][level - 1][6]
    else:
        matrix = oracles[1][level][7]
    sim_tab = []
    for i in range(len(history_next)):
        sim_digit, sim_value = similarity_computation.compute_alignment(history_next[i][1], concat_obj, matrix)
        sim_tab.append(sim_value / similarity_computation.quotient)
        if sim_digit:
            new_char = history_next[i][0]
            return new_char, None, sim_tab, 1
    return None, None, sim_tab, 0


def similarity_signal(oracles, level):
    sim_tab = []
    s_tab = []
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    window = similarity_computation.compute_window_audio(oracles, level, concat_obj)
    actual_object_descriptor = similarity_computation.compute_descriptor(window)
    s_tab.append(actual_object_descriptor)
    for i in range(len(history_next)):
        # s_tab corresponds to the descriptors from history_next_table concatenated with the descriptor extracted
        # from actual_obj
        s_tab.append(history_next[i][2])
        sim_digit, sim_value = similarity_computation.compute_signal_similarity(s_tab, i)
        sim_tab.append(sim_value)
        if sim_digit:
            new_char = history_next[i][0]
            return new_char, actual_object_descriptor, sim_tab, 1
    s_tab.pop(0)
    return None, None, sim_tab, 0


def char_next_level_similarity(oracles, level):
    """ The function compare the actual new structured string with structured strings already seen before. For now,
    the strings have to be the exact sames to be considered as similar. The history_next tab is modified according to
    the results and the new string of upper level new_char is returned."""
    # put here the similarity function that interest you
    # similarity_strict
    # similarity_alignment
    # similarity_signal
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    matrix_next = oracles[1][level][6]

    if level == 0:
        matrix = oracles[1][level][7]
    else:
        matrix = oracles[1][level - 1][6]
    if STRICT_EQUALITY:
        new_char, new_descriptor, sim_tab, digit = similarity_strict(oracles, level)
    elif ALIGNMENT:
        new_char, new_descriptor, sim_tab, digit = similarity_alignment(oracles, level)
    else:
        new_char, new_descriptor, sim_tab, digit = similarity_alignment(oracles, level)
    if digit:
        return new_char

    new_char = chr(letter_diff + len(history_next) + 1)
    sim_tab.append(1)
    matrix_next[0] += new_char
    matrix_next[1].append(sim_tab.copy())
    for i in range(len(matrix_next[1]) - 1):
        matrix_next[1][i].append(matrix_next[1][len(matrix_next[1]) - 1][i])

    history_next.append((new_char, concat_obj, new_descriptor))
    return new_char


