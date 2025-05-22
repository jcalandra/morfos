import matplotlib.pyplot as plt
import module_parameters.parameters as prm
import others.object_storage as obj_s
from module_parameters.parameters import processing, EVOL_PRINT, LETTER_DIFF
import numpy as np
f_number = 0
global_factor = 10
figsize= [30, 5]
global color_nb


class FormalDiagramGraph:

    def _print_formal_diagram_init(self, level):
        """ Print the formal diagram at level 'level' at its initialization."""
        fig = plt.figure(figsize=(9, 6))
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
        #plt.xticks(np.arange(0, data_duration_in_s/SR * HOP_LENGTH, 20))
        string = ""
        formal_diagram = mso.levels[level].voices[0].VoiceFD.FormalDiagram.material_lines
        for i in range(len(formal_diagram)):
            string += chr(i + LETTER_DIFF + 1)
        #plt.imshow(formal_diagram, extent=[0, mso.metadata.data_duration_in_s/SR * HOP_LENGTH, len(formal_diagram), 0])
        if processing == 'symbols':
            plt.imshow(formal_diagram, extent=[0, mso.metadata.nb_hop, len(formal_diagram), 0])
        elif processing == 'midi':
            plt.imshow(formal_diagram, extent=[0, mso.metadata.nb_hop/120, len(formal_diagram), 0])
        elif processing == 'signal':
            plt.imshow(formal_diagram, extent=[0, mso.metadata.data_duration_in_s, len(formal_diagram), 0])
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


def final_save_one4all(mso, path_result):
        """ Print the updated formal diagram  'formal_diagram' at level 'level' in the window 'fig_number'."""
    # print("PRINT formal diagram update")
        for level in range(mso.level_max + 1):
            formal_diagram = mso.levels[level].voices[0].VoiceFD.FormalDiagram.material_lines
            len_formal_diagram = len(mso.levels[level].voices[0].VoiceFD.FormalDiagram.material_lines)
            fig_number = mso.levels[level].voices[0].VoiceFD.FormalDiagramGraph.fig_number.number
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
            plt.xticks(np.arange(0, mso.metadata.nb_hop/prm.SR * prm.HOP_LENGTH, 10))

            plt.imshow(formal_diagram, extent=[0, mso.metadata.nb_hop/prm.SR * prm.HOP_LENGTH, len_formal_diagram, 0], cmap='gray')
            plt.savefig(path_result + file_name_pyplot, transparent=True, dpi=1000)
            print("file saved as " + path_result + file_name_pyplot)
            plt.close()


def final_save_all4one(mso, path_result):
        """ Print the updated formal diagram  'formal_diagram' at level 'level' in the window 'fig_number'."""
        # print("PRINT formal diagram update")
        f = plt.figure(figsize=[9,24])
        for level in range(mso.level_max + 1):
            formal_diagram = mso.levels[level].voices[0].VoiceFD.FormalDiagram.material_lines
            len_formal_diagram = len(mso.levels[level].VoiceFD.FormalDiagram.material_lines)
            plt.subplot(mso.level_max + 1, 1, level + 1)
            plt.title("Formal diagram of level " + str(level))
            if processing == 'symbols' or processing == 'vectors':
                plt.xlabel("time in number of states (formal memory)")
            elif processing == 'signal':
                plt.xlabel("time in seconds (formal memory)")
            plt.ylabel("material (material memory)")
            plt.yticks(np.arange(0, len_formal_diagram, 5))
            plt.xticks(np.arange(0, mso.metadata.nb_hop/prm.SR * prm.HOP_LENGTH, 10))
            plt.imshow(formal_diagram, extent=[0, mso.metadata.nb_hop/prm.SR * prm.HOP_LENGTH, len_formal_diagram, 0], cmap='gray')

        file_name_pyplot = 'FD_all.png'
        plt.savefig(path_result + file_name_pyplot, transparent=False, dpi=1000)
        print("file saved as " + path_result + file_name_pyplot)
        plt.close()