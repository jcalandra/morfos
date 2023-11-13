import matplotlib.pyplot as plt
import module_parameters.parameters as prm
import others.object_storage as obj_s
from module_parameters.parameters import processing, EVOL_PRINT, LETTER_DIFF
import numpy as np
f_number = 0
global_factor = 20
figsize= [30, 5]

class FormalDiagram:

    def _formal_diagram_init(self, mso, level):
        """Initialize the formal diagram 'formal_diagram' at level 'level'."""
        if processing == 'signal' and level==0:
            factor = 1
        else:
            factor = global_factor
        new_mat = [1 for i in range(mso.nb_hop*factor)]
        self.material_lines.append(new_mat)
        if level == 0:
            n = 1
            k_end = k_end_link = n
            obj_s.objects_init()
            obj_s.first_occ_init()
        else:
            k_end = k_end_link = 1
            lv = level - 1
            while lv >= 0:
                link = mso.levels[lv].link
                link_r = link.copy()
                link_r.reverse()
                k_end = len(link_r) - link_r.index(k_end) - 1
                if lv == level - 1:
                    k_end_link = k_end
                lv = lv - 1
            n = k_end
        prm.ind_lvl0 = k_end
        self.material_lines[0][0] = 0
        for i in range(1, n*factor):
            self.material_lines[0][i] = 0.7

        # create and update object
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

    def __init__(self):
        self.material_lines = []

    def init(self, mso, level, init_mtx=None):
        if level == -1:
            self.material_lines = [init_mtx]
        else:
            self._formal_diagram_init(mso, level)

    def _formal_diagram_update(self, mso, level):
        """Update the formal diagram 'formal_diagram' at level 'level' at instant 'actual_char_ind' with material
        'actual_char'."""
        if processing == 'signal' and level==0:
            factor = 1
        else:
            factor = global_factor
        actual_char_ind = mso.levels[level].actual_char_ind
        actual_char = mso.levels[level].actual_char - mso.levels[level].oracle.data[1] + 1
        k_init = actual_char_ind
        if level == 0:
            n = k_init_link = k_end_link = 1
        else:
            k_end = k_init
            k_init_link = k_init
            k_end_link = k_init
            lv = level - 1
            while lv >= 0:
                link = mso.levels[lv].link
                link_r = link.copy()
                link_r.reverse()
                k_init = link.index(k_init)
                true_len = len(link) - link_r.index(len(mso.levels[lv + 1].oracle.data) - 1)
                sub_link_r = link.copy()
                sub_link_r = sub_link_r[:true_len]
                sub_link_r.reverse()
                k_end = true_len - sub_link_r.index(k_end) - 1
                if lv == level - 1:
                    k_init_link = k_init
                    k_end_link = k_end
                lv = lv - 1
            n = k_end - k_init + 1
        prm.ind_lvl0 = k_init - 1
        color = 0.7
        if actual_char > len(self.material_lines):
            new_mat = [1 for i in range(mso.nb_hop*factor)]
            self.material_lines.append(new_mat)
            first_occ_mat = (k_init - 1)*(prm.HOP_LENGTH/prm.SR)
            obj_s.first_occ_add_obj(level, first_occ_mat)

        self.material_lines[actual_char - 1][k_init*factor- 1*factor] = 0
        for i in range(1, n*factor):
            self.material_lines[actual_char - 1][factor*k_init+ i - 1*factor] = color

        # create and update object
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

    def update(self, mso, level):
        self._formal_diagram_update(mso, level)


class FormalDiagramGraph:

    def _print_formal_diagram_init(self, level):
        """ Print the formal diagram at level 'level' at its initialization."""
        fig = plt.figure(figsize=(12, 8))
        plt.title("Formal diagram of level " + str(level))
        plt.xlabel("time in seconds (formal memory)")
        plt.ylabel("material (material memory)")
        plt.gray()
        self.fig_number = fig.number

    def __init__(self, level, name, path="cognitive_algorithm_and_its_musical_applications/results/"):
        self.name = ""
        self.path = ""
        self.fig_number = None
        self.set_name(name)
        self.set_path(path)
        self._print_formal_diagram_init(level)

    def set_name(self, name):
        self.name = name

    def set_path(self, path):
        self.path = path

    def _print_formal_diagram_update(self, mso, level):
        """ Print the updated formal diagram  'formal_diagram' at level 'level' in the window 'fig_number'."""
        self.fig_number = plt.figure(level + 1)
        fig = self.fig_number
        plt.clf()
        global f_number
        f_number += 1
        plt.title("Formal diagram of level " + str(level))
        if processing == 'symbols':
            plt.xlabel("time in number of states (formal memory)")
        elif processing == 'signal':
            plt.xlabel("time in seconds (formal memory)")
        plt.ylabel("material (material memory)")
        #plt.yticks(np.arange(0, len(formal_diagram), 5))
        #plt.xticks(np.arange(0, data_length/SR * HOP_LENGTH, 20))
        string = ""
        formal_diagram = mso.levels[level].formal_diagram.material_lines
        for i in range(len(formal_diagram)):
            string += chr(i + LETTER_DIFF + 1)
        #plt.imshow(formal_diagram, extent=[0, mso.data_length/SR * HOP_LENGTH, len(formal_diagram), 0])
        if processing == 'symbols':
            plt.imshow(formal_diagram, extent=[0, mso.nb_hop, len(formal_diagram), 0])
        elif processing == 'signal':
            plt.imshow(formal_diagram, extent=[0, mso.data_length, len(formal_diagram), 0])
        if EVOL_PRINT == 1:
            plt.pause(0.1)
            # name = self.path + self.name + str(
            #     f_number) + ".png"
            # plt.savefig(name)
        if prm.TO_SAVE_PYP:
            path_results = prm.PATH_RESULT
            file_name_pyplot = "FD_level" + str(level)
            plt.savefig(path_results + file_name_pyplot)
        return fig.number

    def update(self, mso, level):
        self._print_formal_diagram_update(mso, level)


def final_save_one4all(mso):
        """ Print the updated formal diagram  'formal_diagram' at level 'level' in the window 'fig_number'."""
    # print("PRINT formal diagram update")
        for level in range(mso.level_max + 1):
            formal_diagram = mso.levels[level].formal_diagram.material_lines
            len_formal_diagram = len(mso.levels[level].formal_diagram.material_lines)
            fig_number = mso.levels[level].formal_diagram_graph.fig_number.number
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
            plt.yticks(np.arange(0, len_formal_diagram, 5))
            plt.xticks(np.arange(0, mso.nb_hop/prm.SR * prm.HOP_LENGTH, 5))

            result_path = prm.PATH_RESULT
            plt.imshow(formal_diagram, extent=[0, mso.nb_hop/prm.SR * prm.HOP_LENGTH, len_formal_diagram, 0], cmap='gray')
            plt.savefig(result_path + file_name_pyplot, transparent=True, dpi=1000)
            print("file saved as " + result_path + file_name_pyplot)
            plt.close()


def final_save_all4one(mso):
        """ Print the updated formal diagram  'formal_diagram' at level 'level' in the window 'fig_number'."""
        # print("PRINT formal diagram update")
        f = plt.figure(figsize=[12,30])
        for level in range(mso.level_max + 1):
            formal_diagram = mso.levels[level].formal_diagram.material_lines
            len_formal_diagram = len(mso.levels[level].formal_diagram.material_lines)
            plt.subplot(mso.level_max + 1, 1, level + 1)
            plt.title("Formal diagram of level " + str(level))
            if processing == 'symbols' or processing == 'vectors':
                plt.xlabel("time in number of states (formal memory)")
            elif processing == 'signal':
                plt.xlabel("time in seconds (formal memory)")
            plt.ylabel("material (material memory)")
            plt.yticks(np.arange(0, len_formal_diagram, 5))
            plt.xticks(np.arange(0, mso.nb_hop/prm.SR * prm.HOP_LENGTH, 5))
            plt.imshow(formal_diagram, extent=[0, mso.nb_hop/prm.SR * prm.HOP_LENGTH, len_formal_diagram, 0], cmap='gray')

        file_name_pyplot = 'FD_all.png'
        result_path = prm.PATH_RESULT
        plt.savefig(result_path + file_name_pyplot, transparent=False, dpi=1000)
        print("file saved as " + result_path + file_name_pyplot)
        plt.close()