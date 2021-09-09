import oracle_mso
import class_materials
import class_formal_diagrams
import class_object
from parameters import SR

from data_computing import get_data


class MSO:
    """ The Multi-Scale Oracle"""

    def __init__(self, name, audio_path):
        self.name = ""
        self.set_name(name)
        self.level_max = -1
        self.levels = []

        self.audio = []
        self.get_audio(audio_path)
        self.rate = SR
        self.data_length = 0
        self.data_size = 0

    def set_name(self, name):
        self.name = name

    def get_audio(self, audio_path):
        data, rate, data_size, data_length = get_data(audio_path)
        self.data_length = data_length
        self.audio = data
        self.rate = rate
        self.data_size = data_size
        return

    def add_level(self, level):
        self.levels.append(level)
        self.level_max += 1


class MSOLevel:
    """ A specific level of the Multi-Scale Oracle """

    def __init__(self, mso):
        self.objects = []
        self.oracle = None
        self.formal_diagram = None
        self.formal_diagram_graph = class_formal_diagrams.FormalDiagramGraph(0, mso.name)
        self.link = [0]
        self.materials = class_materials.Materials()
        self.concat_obj = class_object.ConcatObj()
        mso.add_level(self)

    def init_oracle(self, flag, teta, dim):
        self.oracle = oracle_mso.create_oracle(flag, threshold=teta, dfunc='cosine', dfunc_handle=None, dim=dim)

    def init_formal_diagram(self, mso, level, init_mtx):
        self.formal_diagram = class_formal_diagrams.FormalDiagram(mso, level, init_mtx)

    def update_objects(self, obj):
        self.objects.append(obj)

    def update_oracle(self, data):
        self.oracle.add_state(data)

    def update_link(self, node):
        self.objects.append(node)

    def update_similarity(self, mso, obj, data, level):
        self.update_oracle(data)
        self.update_objects(obj)
        self.formal_diagram.update(obj.label, obj.id, mso, level)
        self.formal_diagram_graph.update(mso, level)
        self.concat_obj.update(obj)

    def update_segmentation(self, obj, sim_tab, node):
        self.materials.update(obj.rep, self.concat_obj, sim_tab)
        for i in range(len(self.concat_obj)):
            self.update_link(node)
