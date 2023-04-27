import matplotlib.pyplot as plt
import matplotlib.figure as fg
import parameters as prm
import numpy as np
import objects_storage as obj_s
from mpl_toolkits.mplot3d import Axes3D

# In this file are implemented all the fonctions for the initialization and the update of the formal diagram and
# the functions to display the formal diagrams.
SR = prm.SR
HOP_LENGTH = prm.HOP_LENGTH
TO_SAVE_PYP = prm.TO_SAVE_PYP
path_results = prm.PATH_RESULT
EVOL_PRINT = prm.EVOL_PRINT

letter_diff = prm.LETTER_DIFF
processing = prm.processing

f_number = 0
figsize= [30, 5]
global_factor = 20


# ============================================ FORMAL DIAGRAM 2D =======================================================
# Implementation for an evolutive formal diagram
def print_formal_diagram_init(level):
    """ Print the formal diagram at level 'level' at its initialization."""
    # print("PRINT formal diagram init")
    if prm.TO_SHOW_PYP:
        fig = plt.figure(figsize= figsize)
        plt.title("Formal diagram of level " + str(level))
        plt.xlabel("time in seconds (formal memory)")
        plt.ylabel("material (material memory)")
        plt.gray()
        return fig.number
    else:
        return 0


def print_formal_diagram_update(fig_number, level, formal_diagram, data_length):
    """ Print the updated formal diagram  'formal_diagram' at level 'level' in the window 'fig_number'."""
    # print("PRINT formal diagram update")
    if prm.TO_SHOW_PYP:
        fig = plt.figure(fig_number, figsize=figsize)
        plt.clf()
        global f_number
        f_number += 1
        file_name_pyplot = "FD_level" + str(level)
        plt.title("Formal diagram of level " + str(level))
        if processing == 'symbols' or processing == 'vectors':
            plt.xlabel("time in number of states (formal memory)")
        elif processing == 'signal':
            plt.xlabel("time in seconds (formal memory)")
        plt.ylabel("material (material memory)")
        plt.yticks(np.arange(0, len(formal_diagram), 5))
        plt.xticks(np.arange(0, data_length/SR * HOP_LENGTH, 20))
        string = ""
        for i in range(len(formal_diagram)):
            string += chr(i + letter_diff + 1)
        # plt.yticks([i for i in range(len(string))], string)
        plt.imshow(formal_diagram, extent=[0, data_length/SR * HOP_LENGTH, len(formal_diagram), 0])
        if TO_SAVE_PYP:
            plt.savefig(path_results + file_name_pyplot)
        if EVOL_PRINT == 1:
            plt.pause(0.1)
            if TO_SAVE_PYP:
                name = "cognitive_algorithm_and_its_musical_applications/src/oracle_version/figures_TENOR/" + str(f_number) \
                       + ".png"
                plt.savefig(name)
        return fig.number
    else:
        return 0


def formal_diagram_init_nobound(formal_diagram, data_length, oracles, level):
    """Initialize the formal diagram 'formal_diagram' at level 'level'."""
    # print("formal diagram init")
    new_mat = [1 for i in range(data_length)]
    formal_diagram.append(new_mat)
    if level == 0:
        n = k_end_link = 1
        obj_s.objects_init()
        obj_s.first_occ_init()
    else:
        k_end = k_end_link = 1
        lv = level - 1
        while lv >= 0:
            link = oracles[1][lv][1]
            link_r = link.copy()
            link_r.reverse()
            k_end = len(link_r) - link_r.index(k_end) - 1
            if lv == level - 1:
                k_end_link = k_end
            lv = lv - 1
        n = k_end
    for i in range(n):
        formal_diagram[0][i] = 1.1/4

    obj_s.objects_add_level()
    obj_s.first_occ_add_level()
    links = []
    for i in range(k_end_link):
        links.append(i)
    if processing == 'signal':
        sound = obj_s.data[0:n*prm.HOP_LENGTH]
    else:
        # No sound when character string analysis
        sound = [0]
    id = 0
    mat_num = 0
    x = n*(1/prm.SR)*prm.HOP_LENGTH
    y = 0
    z = n*(1/prm.SR)*prm.HOP_LENGTH
    obj_s.objects_add_new_obj(id, links, x, y, z, mat_num, level, sound)
    obj_s.first_occ_add_obj(level, y)
    return 1


def formal_diagram_update_nobound(formal_diagram, data_length, actual_char, actual_char_ind, oracles, level):
    """Update the formal diagram 'formal_diagram' at level 'level' at instant 'actual_char_ind' with material
    'actual_char'."""
    # print("formal diagram update")
    k_init = actual_char_ind
    if processing == 'symbols':
        actual_char = actual_char - oracles[1][level][0].data[1] + 1
    if level == 0:
        n = k_init_link = k_end_link = 1
    else:
        k_end = k_init
        k_init_link = k_init
        k_end_link = k_init
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
            if lv == level - 1:
                k_init_link = k_init
                k_end_link = k_end
            lv = lv - 1
        n = k_end - k_init + 1
    color = (actual_char_ind % 4 + 0.1)/4
    if actual_char > len(formal_diagram):
        new_mat = [1 for i in range(data_length)]
        formal_diagram.append(new_mat)
        first_occ_mat = (k_init - 1)*(prm.HOP_LENGTH/prm.SR)
        obj_s.first_occ_add_obj(level, first_occ_mat)
    if prm.POLYPHONY and prm.processing == 'signal':
        side_materials(oracles, level, formal_diagram, actual_char, n, k_init)
    for i in range(n):
        formal_diagram[actual_char - 1][k_init + i - 1] = color

    links = []
    for i in range(k_init_link - 1, k_end_link):
        links.append(i)
    if processing == 'signal':
        sound = obj_s.data[k_init*prm.HOP_LENGTH:(k_init + n)*prm.HOP_LENGTH] # remarque: il manque les derniers 1024 échantillons
    else:
        # No sound when character string analysis
        sound = [0]
    id = actual_char_ind - 1
    mat_num = actual_char - 1
    x = (k_init + n - 1)*(prm.HOP_LENGTH/prm.SR)
    y = obj_s.first_occ[level][mat_num]
    z = n*(1/prm.SR)*prm.HOP_LENGTH
    obj_s.objects_add_new_obj(id, links, x, y, z, mat_num, level, sound)
    return 0


def side_materials(oracles, level, formal_diagram, actual_char, n, k_init):
    if level == 0:
        matrix_values = oracles[1][0][7][1]
    else:
        matrix_values = oracles[1][level - 1][6][1]
    for i in range(1, actual_char - 1):
        for j in range(n):
            formal_diagram[i][k_init + j - 1] = min((1 - matrix_values[actual_char - 1][i])/(1 - prm.min_matrix), 1)


def final_save_one4all(oracles, data_length, result_path):
    """ Print the updated formal diagram  'formal_diagram' at level 'level' in the window 'fig_number'."""
    # print("PRINT formal diagram update")
    for level in range(len(oracles[1])):
        formal_diagram = oracles[1][level][4]
        fig_number = oracles[1][level][5]
        fig = plt.figure(fig_number, figsize=figsize)
        plt.clf()
        global f_number
        f_number += 1
        file_name_pyplot = "FD_level" + str(level)
        plt.title("Formal diagram of level " + str(level))
        if processing == 'symbols' or processing == 'vectors':
            plt.xlabel("time in number of states (formal memory)")
        elif processing == 'signal':
            plt.xlabel("time in seconds (formal memory)")
        plt.ylabel("material (material memory)")
        plt.yticks(np.arange(0, len(formal_diagram), 5))
        plt.xticks(np.arange(0, data_length/SR * HOP_LENGTH, 5))
        plt.imshow(formal_diagram, extent=[0, data_length/SR * HOP_LENGTH, len(formal_diagram), 0], cmap='gray')
        plt.savefig(result_path + file_name_pyplot, transparent=True, dpi=1000)
        print("file saved as " + result_path + file_name_pyplot)
        plt.close()
    return 1

def final_save_all4one(oracles, data_length, result_path):
    """ Print the updated formal diagram  'formal_diagram' at level 'level' in the window 'fig_number'."""
    # print("PRINT formal diagram update")
    f = plt.figure(figsize=[12,30])
    for level in range(len(oracles[1])):
        plt.subplot(len(oracles[1]), 1, level + 1)
        formal_diagram = oracles[1][level][4]
        plt.title("Formal diagram of level " + str(level))
        if processing == 'symbols' or processing == 'vectors':
            plt.xlabel("time in number of states (formal memory)")
        elif processing == 'signal':
            plt.xlabel("time in seconds (formal memory)")
        plt.ylabel("material (material memory)")
        plt.yticks(np.arange(0, len(formal_diagram), 5))
        plt.xticks(np.arange(0, data_length/SR * HOP_LENGTH, 5))
        plt.imshow(formal_diagram, extent=[0, data_length/SR * HOP_LENGTH, len(formal_diagram), 0], cmap='gray')

    file_name_pyplot = 'FD_all.png'
    plt.savefig(result_path + file_name_pyplot, transparent=False, dpi=1000)
    print("file saved as " + result_path + file_name_pyplot)
    plt.close()
    return 1


def formal_diagram_init(formal_diagram, data_length, oracles, level):
    """Initialize the formal diagram 'formal_diagram' at level 'level'."""
    # print("formal diagram init")
    if processing == 'signal' and level==0:
        factor = 1
    else:
        factor = global_factor
    new_mat = [1 for i in range(data_length*factor)]
    formal_diagram.append(new_mat)
    if level == 0:
        n = k_end_link = 1
        obj_s.objects_init()
        obj_s.first_occ_init()
    else:
        k_end = k_end_link = 1
        lv = level - 1
        while lv >= 0:
            link = oracles[1][lv][1]
            link_r = link.copy()
            link_r.reverse()
            k_end = len(link_r) - link_r.index(k_end) - 1
            if lv == level - 1:
                k_end_link = k_end
            lv = lv - 1
        n = k_end
    formal_diagram[0][0] = 0
    for i in range(1, n*factor):
        formal_diagram[0][i] = 0.7

    obj_s.objects_add_level()
    obj_s.first_occ_add_level()
    links = []
    for i in range(k_end_link):
        links.append(i)
    if processing == 'signal':
        sound = obj_s.data[0:n*prm.HOP_LENGTH]
    else:
        # No sound when character string analysis
        sound = [0]
    id = 0
    mat_num = 0
    x = n*(1/prm.SR)*prm.HOP_LENGTH
    y = 0
    z = n*(1/prm.SR)*prm.HOP_LENGTH
    obj_s.objects_add_new_obj(id, links, x, y, z, mat_num, level, sound)
    obj_s.first_occ_add_obj(level, y)
    return 1


def formal_diagram_update(formal_diagram, data_length, actual_char, actual_char_ind, oracles, level):
    """Update the formal diagram 'formal_diagram' at level 'level' at instant 'actual_char_ind' with material
    'actual_char'."""
    # print("formal diagram update")
    if processing == 'signal' and level==0:
        factor = 1
    else:
        factor = global_factor
    k_init = actual_char_ind
    if processing == 'symbols':
        actual_char = actual_char - oracles[1][level][0].data[1] + 1
    if level == 0:
        n = k_init_link = k_end_link = 1
    else:
        k_end = k_init
        k_init_link = k_init
        k_end_link = k_init
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
            if lv == level - 1:
                k_init_link = k_init
                k_end_link = k_end
            lv = lv - 1
        n = k_end - k_init + 1
    color = 0.7
    if actual_char > len(formal_diagram):
        new_mat = [1 for i in range(data_length*factor)]
        formal_diagram.append(new_mat)
        first_occ_mat = (k_init - 1)*(prm.HOP_LENGTH/prm.SR)
        obj_s.first_occ_add_obj(level, first_occ_mat)
    if prm.POLYPHONY and prm.processing == 'signal':
        side_materials(oracles, level, formal_diagram, actual_char, n*factor, k_init*factor)
    formal_diagram[actual_char - 1][k_init*factor- 1*factor] = 0
    for i in range(1, n*factor):
        formal_diagram[actual_char - 1][factor*k_init+ i - 1*factor] = color

    links = []
    for i in range(k_init_link - 1, k_end_link):
        links.append(i)
    if processing == 'signal':
        sound = obj_s.data[k_init*prm.HOP_LENGTH:(k_init + n)*prm.HOP_LENGTH] # remarque: il manque les derniers 1024 échantillons
    else:
        # No sound when character string analysis
        sound = [0]
    id = actual_char_ind - 1
    mat_num = actual_char - 1
    x = (k_init + n - 1)*(prm.HOP_LENGTH/prm.SR)
    y = obj_s.first_occ[level][mat_num]
    z = n*(1/prm.SR)*prm.HOP_LENGTH
    obj_s.objects_add_new_obj(id, links, x, y, z, mat_num, level, sound)
    return 0


# ======================================== FORMAL DIAGRAM 3D (TESTS) ===================================================
def diagram3D(oracles):
    """ 3D representation proposition of the formal diagrams once they are all created."""
    z_len = len(oracles[1])
    y_len = len(oracles[1][0][4][0])

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