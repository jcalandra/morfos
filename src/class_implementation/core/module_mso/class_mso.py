import oracle_mso
from mso import class_materialsMemory
from core.module_visualization import class_fd2DVisu
from object_model import class_object
from parameters import SR, HOP_LENGTH

from data_computing import get_data


class MSO:
    """ The Multi-Scale Oracle"""

    def __init__(self, name):
        self.name = ""
        self.set_name(name)
        self.level_max = -1
        self.levels = []

        self.audio = []
        self.symbol = ""
        self.rate = SR
        self.data_length = 0
        self.data_size = 0
        self.nb_hop = 0
        self.end_mk = 0

        self.matrix = class_materialsMemory.SimMatrix()

    def set_name(self, name):
        self.name = name

    def get_audio(self, audio_path):
        data, rate, data_size, data_length = get_data(audio_path)
        self.data_length = data_length
        for i in range(len(data)):
            self.audio.append(data[i])
        self.rate = rate
        self.data_size = data_size
        self.nb_hop = int(data_size/HOP_LENGTH)

    def update_audio(self, added_data, data_length, nb_hop):
        self.data_length = data_length
        self.audio = added_data.tolist() + self.audio
        self.nb_hop = nb_hop

    def get_symbol(self, symbol, nb_hop):
        self.symbol = symbol
        self.nb_hop = nb_hop

    def add_level(self, level):
        self.levels.append(level)
        self.level_max += 1


class MSOLevel:
    """ A specific level of the Multi-Scale Oracle """

    def __init__(self, mso):
        self.objects = [class_object.Object()]
        self.oracle = None
        self.formal_diagram = class_fd2DVisu.FormalDiagram()
        self.formal_diagram_graph = class_fd2DVisu.FormalDiagramGraph(0, mso.name)
        self.link = [0]
        self.materials = class_materialsMemory.Materials()
        self.concat_obj = class_object.ConcatObj()

        self.str_obj = ""
        self.actual_char = ""
        self.actual_char_ind = 0
        self.actual_obj = class_object.Object()
        self.iterator = 0
        self.shift = 0

        mso.add_level(self)

    def init_oracle(self, flag, teta=0, dim=1):
        self.oracle = oracle_mso.create_oracle(flag, threshold=teta, dfunc='cosine', dfunc_handle=None, dim=dim)

    def update_objects(self, obj):
        self.objects.append(obj)

    def update_oracle(self, data):
        self.oracle.add_state(data)
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
        self.materials.update(obj.rep, self.concat_obj, sim_tab)
        for i in range(len(self.concat_obj)):
            self.update_link(node)
