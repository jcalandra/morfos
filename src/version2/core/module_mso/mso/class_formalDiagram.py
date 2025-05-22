import module_visualization.class_fd2DVisu as fd2D
import module_parameters.parameters as prm
import others.object_storage as obj_s
from module_parameters.parameters import processing, EVOL_PRINT, LETTER_DIFF
import numpy as np
global_factor = 10


class  FD():
    """ A class to manage the formal diagram of the MSO """
    
    def __init__(self, level):
        self.FormalDiagram = FormalDiagram()
        self.FormalDiagramGraph = fd2D.FormalDiagramGraph(0, "FD Graph of level "+ str(level))

    def print(self):
        self.FormalDiagram.print()


class FormalDiagram:

    def _formal_diagram_init(self, mso, level):
        """Initialize the formal diagram 'formal_diagram' at level 'level'."""
        global color_nb
        color_nb = 0
        if processing == 'signal' or processing == 'midi':
            factor = 1
        else:
            factor = global_factor
        new_mat = [1 for i in range(mso.metadata.nb_hop*factor)]
        self.material_lines.append(new_mat)
        k_end_link = 1
        if level == 0:
            obj_s.objects_init()
            obj_s.first_occ_init()
            
        else:
            lv = level - 1
            link = mso.levels[lv].voices[0].link
            link_r = link.copy()
            link_r.reverse()
            k_end_link = len(link_r) - link_r.index(k_end_link) - 1
        n = mso.levels[level].voices[0].actual_objects[1].extNotes[0].duration
        k_init = 0
        
        prm.ind_lvl0 = k_init + n
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
            sound = obj_s.data.elements.audio[0:n*prm.HOP_LENGTH]
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
        global color_nb
        if processing == 'signal' or processing == 'midi':
            factor = 1
        else:
            factor = global_factor
        actual_char_ind = mso.levels[level].voices[0].actual_char_ind
        actual_char = mso.levels[level].voices[0].actual_char - mso.levels[level].voices[0].oracle.data[1] + 1
        if level == 0:
            k_init_link = k_end_link = 1
        else:
            k_end_link =  k_init_link = actual_char_ind
            lv = level - 1
            link = mso.levels[lv].voices[0].link
            link_r = link.copy()
            link_r.reverse()
            k_init_link = link.index(k_init_link)
            true_len = len(link) - link_r.index(len(mso.levels[lv + 1].voices[0].oracle.data) - 1)
            sub_link_r = link.copy()
            sub_link_r = sub_link_r[:true_len]
            sub_link_r.reverse()
            k_end_link = true_len - sub_link_r.index(k_end_link) - 1
        n = mso.levels[level].voices[0].actual_objects[actual_char_ind].extNotes[0].duration
        k_init = mso.levels[level].voices[0].total_duration - n

        


        prm.ind_lvl0 = k_init
        color = 0.7
        color_nb += 1
        if actual_char > len(self.material_lines):
            new_mat = [1 for i in range(mso.metadata.nb_hop*factor)]
            self.material_lines.append(new_mat)
            first_occ_mat = (k_init)*(prm.HOP_LENGTH/prm.SR)
            obj_s.first_occ_add_obj(level, first_occ_mat)

        self.material_lines[actual_char - 1][k_init*factor] = 0
        for i in range(1, n*factor):
            self.material_lines[actual_char - 1][factor*k_init + i] = color #(color_nb%4 + 0.3)/4

        # create and update object
        links = []
        for i in range(k_init_link - 1, k_end_link):
            links.append(i)
        if processing == 'signal':
            sound = obj_s.data.elements.audio[k_init*prm.HOP_LENGTH:(k_init + n)*prm.HOP_LENGTH] # remarque: il manque les derniers 1024 échantillons
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

    def print(self):
        """ Print the formal diagram."""
        for i in range(len(self.material_lines)):
            print("line " + str(i) + ": ", end="")
            for j in range(len(self.material_lines[i])):
                print(str(self.material_lines[i][j]) + " ", end="")
            print()

