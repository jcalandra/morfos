from numpy import load
from qmatrix import qmatrix as qm
import parameters
import main_mso_char

# First protocol:
# 1) Apply a filter to obtain 1 while upper value and 0 otherwise
# 2) Reorder the materials by order of appearance of the materials
# 3) Extract a symbolic string


def qmat_protocol1(qmat):
    """ Apply the first protocol:
    1) Apply a filter to obtain 1 while upper value and 0 otherwise
    2) Reorder the materials by order of appearance of the materials
    3) Extract a symbolic string
    """
    qmatrix_inter = qm.qmat_binary_filter(qmat)
    qmatrix_inter2 = qm.qmat_reorder_materials(qmatrix_inter)
    qmat_symbols = qm.qmat_symbolic_string(qmatrix_inter2)
    return qmat_symbols, qmatrix_inter2, qmatrix_inter


def main():
    path = "/data/qmatrix"
    for song in range(71,101):
        if song < 10:
            number = '0' + str(song)
        else:
            number = str(song)
        result_path = parameters.project_root + '/results/qmatrix/exp1/rwcpop/Pop ' + number +'/'
        q_matrix = load(f"{path}/Qmatrix_song{song}.npy", allow_pickle=True)
        qmat_symbols, qmatrix_inter2, qmatrix_inter = qmat_protocol1(q_matrix)
        main_mso_char.main(qmat_symbols, result_path)

# main()
