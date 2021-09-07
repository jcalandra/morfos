import oracle_mso
import class_materials
import class_formal_diagrams
import class_object

from data_computing import get_data


class MSO:
    """ The Multi-Scale Oracle"""

    def __init__(self, name, audio_path):
        self.name = ""
        self.set_name(name)
        self.level_max = -1
        self.data_length = 0
        self.audio = []
        self.get_audio(audio_path)
        self.levels = []

    def set_name(self, name):
        self.name = name

    def get_audio(self, audio_path):
        data, rate, data_size, data_length = get_data(audio_path)
        self.data_length = data_length
        self.audio = data
        return

    def add_level(self, level):
        self.levels.append(level)
        self.level_max += 1


class MSOLevel:
    """ A specific level of the Multi-Scale Oracle """

    def __init__(self, flag, mso, level):
        self.objects = []
        self.oracle = oracle_mso.create_oracle(flag)
        self.formal_diagram = class_formal_diagrams.FormalDiagram(mso, level)
        self.formal_diagram_graph = class_formal_diagrams.FormalDiagramGraph(0, mso.name)
        self.link = [0]
        self.materials = class_materials.Materials()
        self.concat_obj = class_object.ConcatObj()

    def update_objects(self, obj):
        self.objects.append(obj)

    def update_oracle(self, data):
        self.oracle.add_state(data)

    def update_link(self, node):
        self.objects.append(node)

    def update_similarity(self, mso, obj, data, level, actual_char, actual_char_ind):
        self.update_oracle(data)
        self.update_objects(obj)
        self.formal_diagram.update(actual_char, actual_char_ind, mso, level)
        self.formal_diagram_graph.update(mso, level)
        self.concat_obj.update()

    def update_segmentation(self, obj, sim_tab, node):
        self.materials.update(obj.rep, self.concat_obj, sim_tab)
        for i in range(len(self.concat_obj)):
            self.update_link(node)
