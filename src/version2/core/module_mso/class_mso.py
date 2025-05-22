import module_mso.mso.oracle.class_oracle as class_oracle
from module_mso.mso import class_materialsMemory
from core.module_visualization import class_fd2DVisu
from object_model import class_object
import class_concatObj
import module_parameters.parameters as prm
import matplotlib.pyplot as plt
import math
import criterias.module_precomputing.precomputer as pc
import module_mso.mso.class_formalDiagram as class_fd

from module_parameters.parameters import SR, HOP_LENGTH, teta, NB_VALUES


def mso_init(name, cdata):
    """ Initialise the MSO """

    mso = MSO(name)
    mso.set_data_from_cdata(cdata)
    mso.set_metadata_from_cdata(cdata)

    return mso


class MSO:
    """ The Multi-Scale Oracle"""

    def __init__(self, name):
        self.name = ""
        self.set_name(name)
        self.level_max = -1
        self.levels = []

        self.data = Data()
        self.metadata = Metadata()
        self.end_mk = 0 
        self.out = 0
        self.segmentations = []
        self.matrix = class_materialsMemory.Materials()

# setters
    def set_name(self, name):
        self.name = name

    def set_level_max(self, level_max):
        self.level_max = level_max

    def set_data(self, data):
        self.data = data

    def set_metadata(self, metadata):
        self.metadata = metadata
    
    def set_data_from_cdata(self, cdata):
        if prm.processing == "signal":
            self.data.set_audio_from_cdata(cdata)
        if prm.processing == "symbols":
            self.data.set_symbol_from_cdata(cdata)
        if prm.processing == "midi":
            self.data.set_midi_from_cdata(cdata)

    def set_metadata_from_cdata(self, cdata):
        if prm.processing == "signal":
            self.metadata.set_audio_from_cdata(cdata)
        if prm.processing == "symbols":
            self.metadata.set_symbol_from_cdata(cdata)
        if prm.processing == "midi":
            self.metadata.set_midi_from_cdata(cdata)
        self.metadata.print()
    
    def set_end_mk(self, end_mk):
        self.end_mk = end_mk

    def set_out(self, out):
        self.out = out
    
    def set_segmentation(self, seg):
        self.segmentation = seg

    def set_matrix(self, matrix):
        self.matrix = matrix

# getters

    def get_segmentation(self, seg):
        self.segmentations = [seg]

    def add_level(self, level):
        self.levels.append(level)
        self.level_max += 1

    #TODO: @jcalandra 20/05/2025 delete or reimplement
    def update_audio(self, added_data, data_duration_in_s, nb_hop):
        self.metadata.data_duration_in_s = data_duration_in_s
        self.data.audio = added_data.tolist() + self.audio
        self.metadata.nb_hop = nb_hop

    def update_segmentation(self, seg):
        self.segmentations.append(seg)

    def update_out(self, bool):
        self.out = bool

    def reset_levels(self): #TODO: simplify the code
        plt.close('all')
        self.name = ""
        self.set_name(self.name)
        self.level_max = -1
        self.levels = []

        self.data = self.data
        self.metadata = self.metadata
        self.end_mk = 0
        self.out = 0
        self.matrix = class_materialsMemory.Materials()

    def reset(self, name):  #TODO: simplify the code
        plt.close('all')
        self.name = ""
        self.set_name(name)
        self.level_max = -1
        self.levels = []

        self.data = self.data.reset()
        self.metadata = self.metadata.reset()
        self.end_mk = 0
        self.segmentations = []
        self.matrix = class_materialsMemory.Materials()

    def print(self):
        print("name", self.name)
        print("level max", self.level_max)
        # print levels
        self.data.print()
        self.metadata.print()
        print("segmentations", self.segmentations)


class Data:
    """ Data of the MSO """

    def __init__(self):
        self.audio = []
        self.symbol = ""
        self.midi = []

# setters
    def set_audio(self, audio):
        self.audio = audio

    def set_symbol(self, symbol):
        self.symbol = symbol

    def set_midi(self, midi):
        self.midi = midi

    def set_audio_from_cdata(self, cdata):
        audio = cdata.input_data.elements.audio
        for i in range(prm.NB_SILENCE):
            self.audio.append(0)
        for i in range(len(audio)):
            self.audio.append(audio[i]) 

    def set_symbol_from_cdata(self, cdata):
        symbol = cdata.input_data
        self.set_symbol(symbol)

    def set_midi_from_cdata(self, cdata):
        self.set_midi(cdata.input_data)

# getters
    def get_audio(self):
        return self.audio
    
    def get_symbol(self):
        return self.symbol
    
    def get_midi(self):
        return self.midi
    
# printing
    def print(self):
        print("audio", self.audio)
        print("symbol", self.symbol)
        print("midi", self.midi)

# reset
    def reset(self):
        self.audio = []
        self.symbol = ""
        self.midi = []


class Metadata:
    """ Metadata of the MSO """

    def __init__(self):
        self.rate = 0
        self.data_duration_in_s = 0
        self.data_size = 0
        self.nb_hop = 0
        self.dims = 1

# setters
    def set_rate(self, rate):
        self.rate = rate

    def set_data_duration_in_s(self, data_duration_in_s):
        self.data_duration_in_s = data_duration_in_s

    def set_data_size(self, data_size):
        self.data_size = data_size

    def set_nb_hop(self, nb_hop):
        self.nb_hop = nb_hop

    def set_dims(self, dims):
        self.dims = dims

    def set_audio_from_cdata(self, cdata):
        audio = cdata.input_data.elements.audio
        data_size = len(audio)
        self.set_rate(prm.SR)
        self.set_data_size(data_size + prm.NB_SILENCE)
        self.set_nb_hop(math.ceil(data_size/HOP_LENGTH))
        self.set_data_duration_in_s(data_size/self.rate)
        self.set_dims(cdata.dim)

    def set_symbol_from_cdata(self, cdata):
        symbol = cdata.input_data
        self.set_nb_hop(cdata.input_data.length)
        self.set_dims(cdata.dim)


    def set_midi_from_cdata(self, cdata):
        duration = cdata.input_data.duration
        sum_duration = 0
        for i in range(len(duration)):
            sum_duration += duration[i]
        self.set_nb_hop(sum_duration)
        self.set_dims(cdata.dim)


# getters
    def get_rate(self):
        return self.rate
    
    def get_data_duration_in_s(self):
        return self.data_duration_in_s 

    def get_data_size(self):
        return self.data_size
    
    def get_nb_hop(self):
        return self.nb_hop
    
    def get_dims(self):
        return self.dims

# printing
    def print(self):
        print("rate", self.rate)
        print("data_duration_in_s", self.data_duration_in_s)
        print("data_size", self.data_size)
        print("nb_hop", self.nb_hop)
        print("dims", self.dims)

# reset
    def reset(self):
        self.rate = 0
        self.data_duration_in_s = 0
        self.data_size = 0
        self.nb_hop = 0
        self.dims = 1      


class MSOLevel:
    """ A specific level of the Multi-Scale Oracle """

    def __init__(self, mso):
        #self.objects = [class_object.Object()] #TODO: @jcalandra 20/05/2025 to delete when realtime implemented
        self.level = mso.level_max + 1
        self.voices = []

        #self.oracle = None
        #self.actual_objects = [class_object.Object()] #TODO: @jcalandra 20/05/2025 to integrate in the oracle
        #self.total_duration = 0

        self.GeneralFD = class_fd.FD(self.level)
        self.GeneralMaterials = class_materialsMemory.Materials()

        #self.link = [0] 
        #self.concat_obj = class_concatObj.ConcatObj()

  
        #self.actual_char = ""
        #self.actual_char_ind = 0
        #self.actual_obj = class_object.Object()
        #self.iterator = 0
        #self.shift = 0

        mso.add_level(self)

# setters
    def set_level(self, level):
        self.level = level
    def set_voices(self, voices):
        self.voices = voices
    def set_generalFD(self, GeneralFD):
        self.GeneralFD = GeneralFD
    def set_materials(self, materials):
        self.GeneralMaterials = materials

# getters
    def get_level(self):
        return self.level
    def get_voices(self):
        return self.voices
    def get_generalFD(self):
        return self.GeneralFD
    def get_materials(self):
        return self.GeneralMaterials
    
# update

    def update_similarity(self, mso, level):
        self.GeneralFD.FormalDiagram.update(mso, level)
        self.GeneralFD.FormalDiagramGraph.update(mso, level)

    def update_segmentation(self, obj, sim_tab):
        self.GeneralMaterials.update(obj.rep, self.concat_obj, obj.extNotes[0].note.descriptors, sim_tab)

    def compute_stab(self):
        stab = [[],[],[]]
        for obj in self.objects:
            stab[0].append(obj.extNotes[0].note.descriptors.concat_descriptors)
            stab[1].append(obj.extNotes[0].note.descriptors.mean_descriptors)
            stab[2].append(obj.extNotes[0].note.label)
        return stab
    
    def add_voice(self, voice):
        self.voices.append(voice)

# printing
    def print(self):
        print("general formal diagram", self.GeneralFD.print())
        print("general history next", self.GeneralMaterials.history)
        print("general matrix_next",  self.GeneralMaterials.sim_matrix)


class Voice:
    """ A specific voice of the Multi-Scale Oracle Level """

    def __init__(self, msolevel):
        self.level = msolevel.level
        self.objects = [class_object.Object()] #TODO: @jcalandra 20/05/2025 to delete when realtime implemented

        self.oracle = None
        self.actual_objects = [class_object.Object()] #TODO: @jcalandra 20/05/2025 to integrate in the oracle
        self.total_duration = 0
        self.link = [0] 
        self.concat_obj = class_concatObj.ConcatObj()
        self.VoiceMaterials = class_materialsMemory.Materials()
        self.VoiceFD = class_fd.FD(self.level)

        self.actual_char = ""
        self.actual_char_ind = 0
        self.actual_obj = class_object.Object()
        self.iterator = 0
        self.shift = 0

        msolevel.add_voice(self)

#initialisation
    def init_oracle(self, flag, teta=teta, dim=1):
        self.oracle = class_oracle.create_oracle(flag, threshold=teta, dfunc='cosine', dfunc_handle=None, dim=dim)

# setters
    def set_level(self, level):
        self.level = level
    def set_objects(self, objects):
        self.objects = objects
    def set_oracle(self, oracle):
        self.oracle = oracle
    def set_actual_objects(self, actual_objects):
        self.actual_objects = actual_objects
    def set_total_duration(self, total_duration):
        self.total_duration = total_duration
    def set_link(self, link):
        self.link = link
    def set_concat_obj(self, concat_obj):
        self.concat_obj = concat_obj
    def set_VoiceMaterials(self, VoiceMaterials):   
        self.VoiceMaterials = VoiceMaterials
    def set_VoiceFD(self, VoiceFD):
        self.VoiceFD = VoiceFD
    def set_actual_char(self, actual_char):
        self.actual_char = actual_char
    def set_actual_char_ind(self, actual_char_ind):
        self.actual_char_ind = actual_char_ind
    def set_actual_obj(self, actual_obj):
        self.actual_obj = actual_obj
    def set_iterator(self, iterator):
        self.iterator = iterator
    def set_shift(self, shift): 
        self.shift = shift

# getters
    def get_level(self):
        return self.level
    def get_objects(self):
        return self.objects
    def get_oracle(self):
        return self.oracle
    def get_actual_objects(self):
        return self.actual_objects
    def get_total_duration(self):
        return self.total_duration
    def get_link(self):
        return self.link
    def get_concat_obj(self):
        return self.concat_obj
    def get_VoiceMaterials(self):
        return self.VoiceMaterials
    def get_VoiceFD(self):
        return self.VoiceFD
    def get_actual_char(self):
        return self.actual_char
    def get_actual_char_ind(self):
        return self.actual_char_ind
    def get_actual_obj(self):
        return self.actual_obj
    def get_iterator(self):
        return self.iterator
    def get_shift(self): 
        return self.shift
    
#update 
    def update_objects(self, obj):
        self.objects.append(obj)

    def update_oracle(self, ms_oracle, level):
        #self.volume.append(1) #TODO: update with the correct values
        self.oracle.add_state(ms_oracle, level)
        self.actual_char = self.oracle.data[self.shift + self.iterator + 1]
        self.actual_char_ind = self.shift + self.iterator + 1


    def update_link(self, node):
        self.link.append(node)

    def update_similarity(self, mso, obj, data, level):
        self.update_oracle(data)
        self.update_objects(obj)
        self.VoiceFD.FormalDiagram.update(mso, level)
        self.VoiceFD.FormalDiagramGraph.update(mso, level)
        self.concat_obj.update(obj)

    def update_segmentation(self, obj, sim_tab, node):
        self.VoiceMaterials.update(obj.rep, self.concat_obj, obj.extNotes[0].note.descriptors, sim_tab)
        for i in range(self.concat_obj.nb):
            self.update_link(node)
    
# printing 
    def print(self):
        print("level", self.level)
        print("objects", self.objects)

        print("oracle", self.oracle)
        print("actual objects", self.actual_objects)
        print("total duration", self.total_duration)
        print("link", self.link)
        print("concat obj", self.concat_obj)
        print("voice formal diagram", self.GeneralFD.print())
        print("voice history next", self.VoiceMaterials.history)
        print("voice matrix_next",  self.VoiceMaterials.sim_matrix)

        print("actual char", self.actual_char)
        print("actual char ind", self.actual_char_ind)
        print("actual obj", self.actual_obj)
        print("iterator", self.iterator)
        print("shift", self.shift)
    
