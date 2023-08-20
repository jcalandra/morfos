import module_mso.mso.class_oracle as class_oracle
from module_mso.mso import class_materialsMemory
from core.module_visualization import class_fd2DVisu
from object_model import class_object
import class_concatObj
import module_parameters.parameters as prm
import matplotlib.pyplot as plt
import math

from module_parameters.parameters import SR, HOP_LENGTH, teta, NB_VALUES

from module_precomputing.data_computing import get_data


class MSO:
    """ The Multi-Scale Oracle"""

    def __init__(self, name):
        self.name = ""
        self.set_name(name)
        self.level_max = -1
        self.levels = []

        self.init_objects = []
        self.audio = []
        self.symbol = ""
        self.volume = []
        self.rate = SR
        self.data_length = 0
        self.data_size = 0
        self.nb_hop = 0
        self.dims = 1
        self.end_mk = 0
        self.segmentations = []

        self.matrix = class_materialsMemory.Materials()

    def set_name(self, name):
        self.name = name

    def get_audio(self, audio_path):
        data, rate, data_size, data_length = get_data(audio_path)
        for i in range(prm.NB_SILENCE):
            self.audio.append(0)
        for i in range(len(data)):
            self.audio.append(data[i])
        self.rate = rate
        self.data_size = data_size + prm.NB_SILENCE
        self.nb_hop = math.ceil(data_size/HOP_LENGTH + prm.NB_SILENCE/HOP_LENGTH)
        self.data_length = (data_size + prm.NB_SILENCE)/rate

    def get_symbol(self, symbol):
        self.symbol = symbol
        self.nb_hop = len(symbol)

    def get_objects(self, obj):
        self.init_objects = obj

    def get_data(self, data, obj):
        if prm.processing == "signal":
            self.get_audio(data)
        if prm.processing == "symbols":
            self.get_symbol(data)
        self.get_objects(obj)

    def get_segmentation(self, seg):
        self.segmentations = [seg]

    def add_level(self, level):
        self.levels.append(level)
        self.level_max += 1

    def update_audio(self, added_data, data_length, nb_hop):
        self.data_length = data_length
        self.audio = added_data.tolist() + self.audio
        self.nb_hop = nb_hop

    def update_segmentation(self, seg):
        self.segmentations.append(seg)

    def reset_levels(self):
        plt.close('all')
        self.name = ""
        self.set_name(self.name)
        self.level_max = -1
        self.levels = []

        self.init_objects = self.init_objects
        self.audio = self.audio
        self.volume = []
        self.symbol = self.symbol
        self.rate = self.rate
        self.data_length = self.data_length
        self.data_size = self.data_size
        self.nb_hop = self.nb_hop
        self.dims = self.dims
        self.end_mk = 0
        self.segmentations = []

        self.matrix = class_materialsMemory.Materials()

    def reset(self, name):
        plt.close('all')
        self.name = ""
        self.set_name(name)
        self.level_max = -1
        self.levels = []

        self.init_objects = []
        self.init_objects = []
        self.audio = []
        self.volume = []
        self.symbol = ""
        self.rate = SR
        self.data_length = 0
        self.data_size = 0
        self.nb_hop = 0
        self.dims = 1
        self.end_mk = 0
        self.segmentations = []

        self.matrix = class_materialsMemory.Materials()

    def print(self):
        print("name", self.name)
        print("level max", self.level_max)
        # print levels
        print("init objects", [obj.label for obj in self.init_objects])
        print("audio", self.audio)
        print("symbol", self.symbol)
        print("rate", self.rate, "data_length", self.data_length, "data size", self.data_size, "nb hop", self.nb_hop)
        print("segmentations", self.segmentations)


class MSOLevel:
    """ A specific level of the Multi-Scale Oracle """

    def __init__(self, mso):
        self.objects = [class_object.Object()]
        self.oracle = None
        self.formal_diagram = class_fd2DVisu.FormalDiagram()
        self.formal_diagram_graph = class_fd2DVisu.FormalDiagramGraph(0, mso.name)
        self.link = [0]
        self.materials = class_materialsMemory.Materials()
        self.concat_obj = class_concatObj.ConcatObj()
        self.volume = []

        self.actual_objects = [class_object.Object()]
        self.actual_char = ""
        self.actual_char_ind = 0
        self.actual_obj = class_object.Object()
        self.iterator = 0
        self.shift = 0

        mso.add_level(self)

    def init_oracle(self, flag, teta=teta, dim=1):
        self.oracle = class_oracle.create_oracle(flag, threshold=teta, dfunc='cosine', dfunc_handle=None, dim=dim)

    def update_objects(self, obj):
        self.objects.append(obj)

    def update_oracle(self, ms_oracle, level):
        self.volume.append(1)
        self.oracle.add_state(ms_oracle, level)
        self.actual_char = self.oracle.data[self.shift + self.iterator + 1]
        self.actual_char_ind = self.shift + self.iterator + 1


    def update_link(self, node):
        self.objects.append(node)

    def update_similarity(self, mso, obj, data, level):
        self.update_oracle(data)
        self.update_objects(obj)
        self.formal_diagram.update(mso, level)
        self.formal_diagram_graph.update(mso, level)
        self.concat_obj.update(obj)

    def update_segmentation(self, obj, sim_tab, node):
        self.materials.update(obj.rep, self.concat_obj, obj.descriptors, sim_tab)
        for i in range(self.concat_obj.size):
            self.update_link(node)

    def compute_stab(self):
        stab = [[],[],[]]
        for obj in self.objects:
            stab[0].append(obj.descriptors.concat_descriptors)
            stab[1].append(obj.descriptors.mean_descriptors)
            stab[2].append(obj.label)
        return stab

    def print(self):
        print("formal diagram", self.formal_diagram)
        print("link", self.link)
        print("history next", self.materials.history)
        print("matrix_next",  self.materials.sim_matrix)

