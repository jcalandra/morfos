from librosa import cqt, note_to_hz, amplitude_to_db
from numpy import abs, max
from parameters import SR, NB_VALUES, NOTES_PER_OCTAVE


class Object:
    def __init__(self):
        self.signal = []
        self.descriptors = Descriptors()
        self.label = ""
        self.transfo_functions = TransFunctions()
        self.obj_rep = ObjRep()

    def get_signal(self):
        return

    def get_descriptors(self):
        return

    def get_label(self):
        return

    def get_rep(self):
        return


class ConcatObj:
    def __init__(self):
        self.objects = []
        self.concat_signal = []
        self.descriptors = Descriptors()
        self.concat_labels = ""

    def update_objects(self, obj):
        self.objects.append(obj)

    def update_signal(self, signal):
        self.concat_signal += signal

    def update_descriptors(self, new_descriptors):
        for i in len(self.descriptors.concat_descriptors):
            self.descriptors.concat_descriptors[i].append(new_descriptors[i])

        # TODO:
        # @jcalandra 07/09/2021
        # calculer un descripteur moyenné sur toute la partie du signal concernée.
        # Descripteur devrait être une classe à part entière avec le descripteur moyen et les descripteurs concaténés.
        cqt_values = abs(cqt(self.concat_signal, sr=SR, hop_length=len(self.concat_signal),
                                        fmin=note_to_hz('C1'), n_bins=NB_VALUES, bins_per_octave=NOTES_PER_OCTAVE,
                                        window='blackmanharris', sparsity=0.01, norm=1))
        self.descriptors.mean_descriptors = amplitude_to_db(cqt_values, ref=max)

    def update_labels(self, label):
        self.concat_labels += label


class ObjRep:
    def __init__(self):
        self.objects = []


class Descriptors:
    def __init__(self):
        self.concat_descriptors = []
        self.mean_descriptors = []

    def get_concat_descriptors(self, signal):
        return

    def get_mean_descriptors(self, signal):

        return


class TransFunctions:
    def __init__(self):
        self.label_functions = []
        self.descriptor_functions = []