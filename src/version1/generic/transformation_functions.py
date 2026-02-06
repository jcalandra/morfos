import version1.parameters

# penalty values
gap_value = parameters.GAP_VALUE
extend_gap_value = parameters.EXT_GAP_VALUE
gap = parameters.GAP
correc_value = parameters.CORREC_VALUE

letter_diff = parameters.LETTER_DIFF


# ================================== MATERIALS TRANSFORMATION FUNCTIONS ================================================
def identity(mat_rep):
    return mat_rep


def variation(mat_rep, ind_mismatch, value_mismatch):
    mat_obj = mat_rep[:ind_mismatch] + value_mismatch
    if len(mat_rep) > ind_mismatch:
        mat_obj += mat_rep[ind_mismatch + 1:]
    return mat_obj


def reduction(mat_rep, ind_gap, len_gap):
    mat_obj = mat_rep[:ind_gap]
    if len(mat_rep) > ind_gap + len_gap:
        mat_obj += mat_rep[ind_gap + len_gap:]
    return mat_obj


def extension(mat_rep, ind_gap, str_gap):
    mat_obj = mat_rep[:ind_gap] + str_gap
    if len(mat_rep) > ind_gap:
        mat_obj += mat_rep[ind_gap:]
    return mat_obj


def lambda_identity():
    return lambda x: identity(x)


def lambda_variation(ind_mismatch, value_mismatch):
    return lambda x: variation(x, ind_mismatch, value_mismatch)


def lambda_reduction(ind_gap, len_gap):
    return lambda x: reduction(x, ind_gap, len_gap)


def lambda_extension(ind_gap, str_gap):
    return lambda x: extension(x, ind_gap, str_gap)


def lambda_tab_transformation(mat_rep, mat_obj, transfo_tabs, sim_matrix, gap=gap):
    i = 0
    id_mk = 1
    id_ext = id_red = 0
    len_gap = 0
    str_gap = ''
    shift = 0
    len_mat = len(mat_rep)
    while i < len_mat:
        if mat_obj[i] == gap:
            if id_ext == 1:
                transfo_tabs.append([lambda_extension(i - len(str_gap) - shift, str_gap),
                                     'extension', (i - len(str_gap) - shift, str_gap),
                                     gap_value + (len(str_gap) - 1)*extend_gap_value])
                id_ext = 0
                str_gap = ''
            len_gap += 1
            id_mk = 0
            id_red = 1
        elif mat_rep[i] == gap:
            if id_red == 1:
                transfo_tabs.append([lambda_reduction(i - len_gap - shift, len_gap),
                                     'reduction', (i - len_gap - shift, len_gap),
                                     gap_value + (len_gap - 1)*extend_gap_value])
                shift += len_gap
                id_red = 0
                len_gap = 0
            str_gap += mat_obj[i]
            id_mk = 0
            id_ext = 1
        else:
            if id_red == 1:
                transfo_tabs.append([lambda_reduction(i - len_gap - shift, len_gap),
                                     'reduction', (i - len_gap - shift, len_gap),
                                     gap_value + (len_gap - 1)*extend_gap_value])
                shift += len_gap
                id_red = 0
                len_gap = 0
            if id_ext == 1:
                transfo_tabs.append([lambda_extension(i - len(str_gap) - shift, str_gap),
                                     'extension', (i - len(str_gap) - shift, str_gap),
                                     gap_value + (len(str_gap) - 1)*extend_gap_value])
                id_ext = 0
                str_gap = ''
            if mat_rep[i] != mat_obj[i]:
                transfo_tabs.append([lambda_variation(i - shift, mat_obj[i]), 'variation', (i - shift, mat_obj[i]),
                                     1 - sim_matrix[1][ord(mat_rep[i]) - letter_diff]
                                     [(ord(mat_obj[i]) - letter_diff)]])
                id_mk = 0
        i += 1
    if id_red == 1:
        transfo_tabs.append([lambda_reduction(i - len_gap - shift, len_gap),
                             'reduction', (i - len_gap - shift, len_gap),
                             gap_value + (len_gap - 1)*extend_gap_value])
    elif id_ext == 1:
        transfo_tabs.append([lambda_extension(i - len(str_gap) - shift, str_gap),
                             'extension', (i - len(str_gap) - shift, str_gap),
                             gap_value + (len(str_gap) - 1)*extend_gap_value])
    elif id_mk == 1:
        transfo_tabs.append([lambda_identity(), 'identity', (), 0])
    return transfo_tabs


def lambda_get_mat_obj(mat_rep, transfo_tabs):
    mat_obj = mat_rep
    for fun, fun_label, params, weight in transfo_tabs:
        mat_obj = fun(mat_obj)
    return mat_obj


def transformation_similarity(transfo_tabs_ref, transfo_tabs_obj, min_len):
    diff = 1
    for i in range(len(transfo_tabs_ref)):
        diff -= transfo_tabs_ref[i][3]/min_len
        for j in range(len(transfo_tabs_obj)):
            if transfo_tabs_ref[i] == transfo_tabs_obj[j]:
                diff += 2*transfo_tabs_ref[i][3]/min_len
    for j in range(len(transfo_tabs_obj)):
        diff -= transfo_tabs_obj[j][3]/min_len
    return 1 - diff

# ================================= STRUCTURE TRANSFORMATION FUNCTIONS =================================================
