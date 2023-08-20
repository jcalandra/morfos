from numpy import array, load
import qmatrix as qm
import main_mso_char
import parameters


# Second protocol:
# 1) Compute the difference between to consecutive lines
# 2) Apply a filter to obtain 1 while upper value and 0 otherwise
# 3) Reorder the materials by order of appearance of the materials
# 4) Extract a symbolic string


def qmat_diff(qmatrix):
    """ Compute the difference between to consecutive lines """
    qmatrix_diff = array(qmatrix)
    if len(qmatrix_diff > 2):
        qmatrix_diff[0] = abs(qmatrix[1] - qmatrix[0])
    for ind in range(1, len(qmatrix)):
        qmatrix_diff[ind] = abs(qmatrix[ind] - qmatrix[ind - 1])
    return qmatrix_diff


def qmat_protocol2(qmat):
    """ Apply the second protocol:
    1) Compute the difference between to consecutive lines
    2) Apply a filter to obtain 1 while upper value and 0 otherwise
    3) Reorder the materials by order of appearance of the materials
    4) Extract a symbolic string
    """
    qmatrix_diff = qmat_diff(qmat)
    qmatrix_inter = qm.qmat_binary_filter(qmatrix_diff)
    qmatrix_inter2 = qm.qmat_reorder_materials(qmatrix_inter)
    qmat_symbols = qm.qmat_symbolic_string(qmatrix_inter2)
    return qmat_symbols, qmatrix_inter2, qmatrix_inter, qmatrix_diff


def main():
    path = "/data/qmatrix"
    for song in range(1,101):
        if song < 10:
            number = '0' + str(song)
        else:
            number = str(song)
        result_path = parameters.project_root + '/results/qmatrix/exp2/rwcpop/Pop ' + number + '/'
        q_matrix = load(f"{path}/Qmatrix_song{song}.npy", allow_pickle=True)
        qmat_symbols, qmatrix_inter2, qmatrix_inter, qmatrix_diff = qmat_protocol2(q_matrix)
        main_mso_char.main(qmat_symbols, result_path)

# main()
