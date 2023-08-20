import matplotlib.pyplot as plt
from module_parameters.parameters import processing, EVOL_PRINT, LETTER_DIFF
f_number = 0


class FormalDiagram:

    def _formal_diagram_init(self, mso, level):
        """Initialize the formal diagram 'formal_diagram' at level 'level'."""
        new_mat = [1 for i in range(mso.nb_hop)]
        self.material_lines.append(new_mat)
        if level == 0:
            n = 1
        else:
            k_end = 1
            lv = level - 1
            while lv >= 0:
                link = mso.levels[lv].link
                link_r = link.copy()
                link_r.reverse()
                k_end = len(link_r) - link_r.index(k_end) - 1
                lv = lv - 1
            n = k_end
        for i in range(n):
            self.material_lines[0][i] = 1.1 / 4

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
        actual_char_ind = mso.levels[level].actual_char_ind
        k_init = actual_char_ind
        actual_char = mso.levels[level].actual_char - mso.levels[level].oracle.data[1] + 1
        if level == 0:
            n = 1
        else:
            k_end = k_init
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
                lv = lv - 1
            n = k_end - k_init + 1
        color = (actual_char_ind % 4 + 0.1) / 4
        if actual_char > len(self.material_lines):
            new_mat = [1 for i in range(mso.nb_hop)]
            self.material_lines.append(new_mat)
        for i in range(n):
            self.material_lines[actual_char - 1][k_init + i - 1] = color
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
        string = ""
        formal_diagram = mso.levels[level].formal_diagram.material_lines
        for i in range(len(formal_diagram)):
            string += chr(i + LETTER_DIFF + 1)
        # plt.yticks([i for i in range(len(string))], string)
        if processing == 'symbols':
            plt.imshow(formal_diagram, extent=[0, mso.nb_hop, len(formal_diagram), 0])
        elif processing == 'signal':
            plt.imshow(formal_diagram, extent=[0, mso.data_length, len(formal_diagram), 0])
        if EVOL_PRINT == 1:
            plt.pause(0.1)
            name = self.path + self.name + str(
                f_number) + ".png"
            plt.savefig(name)
        #plt.pause(1)
        return fig.number

    def update(self, mso, level):
        self._print_formal_diagram_update(mso, level)
