import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from raw_implementation import parameters


# based on Axel Marmoret code to compute q-matrices
# https://colab.research.google.com/drive/1kdR_FTlqjhfIV1ZyVPi4mcp3htKBaJMn#scrollTo=981418a2


# Plotting
def qmat_plot(qmatrix):
    """ Show the q-matrix with matplotlib.pyplot """
    plt.pcolormesh(np.arange(qmatrix.shape[1]), np.arange(qmatrix.shape[0]), qmatrix, cmap=cm.Greys, shading='auto')
    plt.xlabel("Bar indexes")
    plt.ylabel("Musical patterns")
    plt.gca().invert_yaxis()
    plt.show()


def qmat_plot_transpose(qmatrix):
    """ Show the q-matrix with matplotlib.pyplot """
    plt.pcolormesh(np.arange(qmatrix.shape[0]), np.arange(qmatrix.shape[1]), qmatrix.T, cmap=cm.Greys, shading='auto')
    plt.xlabel("Bar indexes")
    plt.ylabel("Musical patterns")
    plt.gca().invert_yaxis()
    plt.show()


def qmat_binary_filter(qmatrix):
    """ Apply a filter to obtain 1 while upper value and 0 otherwise """
    n = 1
    blank = 1
    while blank == 1:
        for i in range(len(qmatrix[0])):
            if qmatrix[-n][i] != 0:
                blank = 0
        if blank == 1:
            n += 1

    qmatrix = qmatrix[:-n]
    qmat_inter = np.array(qmatrix)
    k = 0
    for i in qmatrix:
        if i.max() != 0:
            max_ind = np.where(i == i.max())[0][0]
        else:
            max_ind = -1
        for j in range(len(i)):
            if j == max_ind:
                qmat_inter[k][j] = 1
            else:
                qmat_inter[k][j] = 0
        k += 1
    return qmat_inter


def qmat_reorder_materials(qmatrix_inter):
    """ Reorder the materials by order of appearance of the materials: corresponds to a formal diagram """
    qmatrix_inter2 = np.array(qmatrix_inter)
    n = len(qmatrix_inter2)
    max_mat = 0
    bool = 0
    for i in range(n):
        # qmat_plot_transpose(qmatrix_inter2)
        if qmatrix_inter2[i].max() != 0:
            max_ind = np.where(qmatrix_inter2[i] == qmatrix_inter2[i].max())[0][0] + bool
        elif i == 0:
            max_ind = 0
            bool = 1
        else:
            if bool:
                max_ind = 0
            else:
                max_ind = -1
        if max_ind >= max_mat:
            qmatrix_int2t = np.array(qmatrix_inter2.T)
            tmp = qmatrix_int2t[max_mat].copy()
            qmatrix_int2t[max_mat] = qmatrix_int2t[max_ind].copy()
            qmatrix_int2t[max_ind] = tmp.copy()
            qmatrix_inter2 = np.array(qmatrix_int2t.T)
            max_mat += 1

    for i in range(n):
        if qmatrix_inter2[i].max() == 0:
            qmatrix_inter2[i][max_mat] = 1
    return qmatrix_inter2


def qmat_symbolic_string(qmatrix_inter2):
    """ Extract a symbolic string from the modified q-matrix"""
    qmat_symbols = ''
    mat_max = -1
    for i in qmatrix_inter2:
        max_ind = np.where(i == i.max())[0][0]
        if max_ind > mat_max:
            mat_max += 1
        qmat_symbols += chr(max_ind + parameters.LETTER_DIFF + 1)
    return qmat_symbols
