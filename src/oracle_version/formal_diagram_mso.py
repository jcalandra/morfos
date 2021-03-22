import matplotlib.pyplot as plt
import parameters as prm
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

SR = prm.SR
HOP_LENGTH = prm.HOP_LENGTH
TO_SAVE_PYP = prm.TO_SAVE_PYP
path_results = prm.PATH_RESULT

letter_diff = prm.LETTER_DIFF


# ============================================ FORMAL DIAGRAM ==========================================================

# First implementation computed at the end of the segmentation function
def cognitive_algorithm(data):
    """ This function creates the matrix that represents the formal diagram produce by the adequated string char. It
    returns the matrix corresponding to the formal diagram and the len of the string."""
    len_data = len(data) - 1
    nb_mat = 1
    new_mat = [1 for i in range(len_data)]
    mtx = [new_mat]
    mtx[0][0] = 0
    for i_hop in range(1, len_data):
        j_mat = data[i_hop + 1] - 1
        if j_mat > len(mtx) - 1:
            nb_mat = nb_mat + 1
            new_mat = [1 for i in range(len_data)]
            mtx.append(new_mat)
            mtx[nb_mat - 1][i_hop] = 0
        else:
            mtx[j_mat][i_hop] = 0
    return mtx, len_data


def graph_cognitive_algorithm(char, matrix, data_length):
    """ plot the picture of formal diagram matrix according to its length data_length. The picture is named ofter the
    string char."""
    name = char
    plt.figure(figsize=(30, 20))
    plt.title("Formal diagram of " + name)
    plt.gray()
    plt.imshow(matrix, extent=[0, data_length, len(matrix), 0])
    plt.show()


# Second implementation for an evolutive formal diagram
def print_formal_diagram_init(level):
    # print("PRINT formal diagram init")
    fig = plt.figure(figsize=(30, 20))
    plt.title("Formal diagram of level " + str(level))
    plt.xlabel("time in seconds (formal memory)")
    plt.ylabel("material (material memory)")
    plt.gray()
    return fig.number


def print_formal_diagram_update(fig_number, level, formal_diagram, data_length):
    # print("PRINT formal diagram update")
    fig = plt.figure(fig_number)
    plt.clf()
    file_name_pyplot = "FD_level" + str(level)
    plt.title("Formal diagram of level " + str(level))
    plt.xlabel("time in seconds (formal memory)")
    plt.ylabel("material (material memory)")
    string = ""
    for i in range(len(formal_diagram)):
        string += chr(i + letter_diff + 1)
    plt.imshow(formal_diagram, extent=[0, int(data_length/SR*HOP_LENGTH), len(formal_diagram), 0])
    #plt.pause(0.0001)
    #plt.savefig(path_results + file_name_pyplot)
    return fig.number


def formal_diagram_init(formal_diagram, data_length, oracles, level):
    # print("formal diagram init")
    new_mat = [1 for i in range(data_length)]
    formal_diagram.append(new_mat)
    if level == 0:
        n = 1
    else:
        k_end = 1
        lv = level - 1
        while lv >= 0:
            link = oracles[1][lv][1]
            link_r = link.copy()
            link_r.reverse()
            k_end = len(link_r) - link_r.index(k_end) - 1
            lv = lv - 1
        n = k_end
    for i in range(n):
        formal_diagram[0][i] = 1.1/4
    return 1


def formal_diagram_update(formal_diagram, data_length, actual_char, actual_char_ind, oracles, level):
    # print("formal diagram update")
    k_init = actual_char_ind
    if level == 0:
        n = 1
    else:
        k_end = k_init
        lv = level - 1
        while lv >= 0:
            link = oracles[1][lv][1]
            link_r = link.copy()
            link_r.reverse()
            k_init = link.index(k_init)
            true_len = len(link) - link_r.index(len(oracles[1][lv + 1][0].data) - 1)
            sub_link_r = link.copy()
            sub_link_r = sub_link_r[:true_len]
            sub_link_r.reverse()
            k_end = true_len - sub_link_r.index(k_end) - 1
            lv = lv - 1
        n = k_end - k_init + 1
    color = (actual_char_ind % 4 + 0.1)/4
    if actual_char > len(formal_diagram):
        new_mat = [1 for i in range(data_length)]
        formal_diagram.append(new_mat)
        for i in range(n):
            formal_diagram[len(formal_diagram) - 1][k_init + i - 1] = color
    else:
        for i in range(n):
            formal_diagram[actual_char - 1][k_init + i - 1] = color
    return 0


def diagram3D(oracles):
    z_len = len(oracles[1])
    y_len = len(oracles[1][0][4][0])
    file_name_pyplot = "FD_3D"

    x_len = len(oracles[1][0][4])
    for i in range(1, z_len):
        if len(oracles[1][0][4]) > x_len:
            nb_mat_max = len(oracles[1][0][4])

    colors = ['red', 'blue', 'green', 'cyan', 'magenta', 'purple', 'grey']
    colors_maxi_mat = []
    colors_mat = []

    maxi_mat = []
    mat = []
    j = 0
    while j < len(oracles[1][0][4]):
        mat_len = []
        colors_len = []
        for k in range(y_len):
            if oracles[1][0][4][j][k][0] == 255 and oracles[1][0][4][j][k][1] == 255 \
                    and oracles[1][0][4][j][k][2] == 255:
                mat_len.append(False)
                colors_len.append(None)
            else:
                mat_len.append(True)
                colors_len.append(colors[0])
        mat.append(mat_len)
        colors_mat.append(colors_len)
        j += 1
    while j < x_len:
        mat_len = [False for i in range(y_len)]
        colors_len = [None for i in range(y_len)]
        mat.append(mat_len)
        colors_mat.append(colors_len)
        j += 1
    maxi_mat.append(mat)
    colors_maxi_mat.append(colors_mat)

    for i in range(1, z_len):
        mat = []
        colors_mat = []
        j = 0
        while j < len(oracles[1][i][4]):
            mat_len = []
            colors_len = []
            for k in range(y_len):
                if (oracles[1][i][4])[j][k] == 1:
                    mat_len.append(False)
                    colors_len.append(None)
                else:
                    mat_len.append(True)
                    colors_len.append(colors[i])
            mat.append(mat_len)
            colors_mat.append(colors_len)
            j += 1
        while j < x_len:
            mat_len = [False for i in range(y_len)]
            colors_len = [None for i in range(y_len)]
            mat.append(mat_len)
            colors_mat.append(colors_len)
            j += 1
        maxi_mat.append(mat)
        colors_maxi_mat.append(colors_mat)
    maxi_mat_np = np.array(maxi_mat)
    maxi_colors_np = np.array(colors_maxi_mat)

    fig = plt.figure(figsize=(50, 50))
    ax = fig.gca(projection='3d')
    ax.voxels(maxi_mat_np, facecolors=maxi_colors_np)
    #plt.savefig(path_results + file_name_pyplot)