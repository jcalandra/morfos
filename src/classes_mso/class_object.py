from librosa import cqt, note_to_hz, amplitude_to_db
from numpy import abs, max
from parameters import SR, NB_VALUES, NOTES_PER_OCTAVE


class Object:
    def __init__(self):
        self.id = None
        self.signal = []
        self.descriptors = Descriptors()
        self.label = ""
        self.transfo_functions = TransFunctions()
        self.obj_rep = ObjRep()

    def get_id(self, ind):
        self.id = ind

    def get_signal(self, signal):
        self.signal = signal

    def get_descriptors(self, descriptors):
        self.descriptors = descriptors

    def get_label(self, label):
        self.label = label

    def get_rep(self, rep):
        self.obj_rep.copy(rep)
        rep.update(self.signal, self.label, self.descriptors)

    def get_similarity(self):
        return

    def update(self, signal, rep):
        self.get_label(signal)
        self.transfo_functions.get_functions()
        self.get_rep(rep)

    def copy(self, obj):
        self.id = obj.id
        self.signal = obj.signal
        self.descriptors.copy(obj.descriptors)
        self.label = obj.label
        self.transfo_functions = obj.transfo_functions
        self.obj_rep.copy(obj.rep)


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

        # TODO: @jcalandra 07/09/2021 mean_descriptors
        #  calculer un descripteur moyenné sur toute la partie du signal concernée.
        #  vérifier que ce qui est obtenu est bien ce que l'on cherche
        cqt_values = abs(cqt(self.concat_signal, sr=SR, hop_length=len(self.concat_signal),
                             fmin=note_to_hz('C1'), n_bins=NB_VALUES, bins_per_octave=NOTES_PER_OCTAVE,
                             window='blackmanharris', sparsity=0.01, norm=1))
        self.descriptors.mean_descriptors = amplitude_to_db(cqt_values, ref=max)

    def update_labels(self, label):
        self.concat_labels += label

    def update(self, obj):
        self.update_objects(obj)
        self.update_signal(obj.signal)
        self.update_descriptors(obj.descriptors)
        self.update_labels(obj.label)


# TODO: @jcalandra 09/09/2021 trajectoire moyenne
#  Définir la "trajectoire audio" moyenne à partir de la DTW
def mean_trajectory(signal_rep, signal):
    return


class ObjRep:
    def __init__(self):
        self.signal = []
        self.label = ""
        self.descriptors = Descriptors()
        self.nb = 0

    def init_signal(self, signal):
        self.signal += signal

    def init_label(self, label):
        self.label += label

    def init_descriptors(self, descriptors):
        self.descriptors.copy(descriptors)

    def init_nb(self):
        self.nb = 1

    def init(self, signal, label, descriptors):
        self.init_signal(signal)
        self.init_label(label)
        self.init_descriptors(descriptors)
        self.init_nb()

    def update_signal(self, signal):
        mean_trajectory(self.signal, signal)

    def update_label(self, label):
        self.label = label

    def update_descriptors(self, descriptors):
        self.nb += 1
        for i in len(self.descriptors.concat_descriptors):
            self.descriptors.concat_descriptors[i] = \
                ((self.nb - 1)*self.descriptors.concat_descriptors[i] + descriptors.concat_descriptors[i])/self.nb
        for i in len(self.descriptors.mean_descriptors):
            self.descriptors.mean_descriptors[i] = \
                ((self.nb - 1)*self.descriptors.mean_descriptors[i] + descriptors.mean_descriptors[i])/self.nb

    def update(self, signal, label, descriptors):
        self.update_signal(signal)
        self.update_label(label)
        self.update_descriptors(descriptors)

    def copy(self, rep):
        self.signal = rep.signal
        self.label = rep.label
        self.descriptors.copy(rep.descriptors)
        self.nb = rep.nb


class Descriptors:
    def __init__(self):
        self.concat_descriptors = []
        self.mean_descriptors = []

    # TODO: @jcalandra 09/09/2021 Descriptors functions
    #  MAJ les fonctions pour la classe descripteurs.
    def get_concat_descriptors(self, signal):
        return

    def get_mean_descriptors(self, signal):
        return

    def get_empty_descriptors(self):
        return

    def update(self, signal):
        self.get_concat_descriptors(signal)
        self.get_mean_descriptors(signal)

    def copy(self, descriptors):
        self.concat_descriptors = descriptors.concat_descriptors
        self.mean_descriptors = descriptors.mean_descriptors


class TransFunctions:
    def __init__(self):
        self.label_functions = []
        self.descriptor_functions = []

    # TODO: @jcalandra 09/09/2021 Transformation functions
    #  MAJ les fonctions pour la classe des fonctions de transformation.
    def get_functions(self):
        return
