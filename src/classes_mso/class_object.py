
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
        self.descriptors.copy(descriptors)

    def get_label(self, label):
        self.label = label

    def get_rep(self, rep):
        self.obj_rep.copy(rep)
        # rep.update(self.signal, self.label, self.descriptors)

    def get_similarity(self):
        return

    def update(self, label, descriptors, signal, rep):
        self.get_label(label)
        self.get_descriptors(descriptors)
        self.get_signal(signal)
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
        self.size = 0

    def init(self, new_obj):
        self.objects = [new_obj]
        self.concat_signal = new_obj.signal
        self.descriptors.copy(new_obj.descriptors)
        self.concat_labels = new_obj.label
        self.size = 1

    def _update_objects(self, obj):
        self.objects.append(obj)

    def _update_signal(self, signal):
        self.concat_signal += signal

    def _update_descriptors(self, new_descriptors):
        for i in range(self.descriptors.nb_descriptors):
            for j in range(len(new_descriptors.concat_descriptors[i])):
                self.descriptors.concat_descriptors[i].append(new_descriptors.concat_descriptors[i][j])
            for j in range(len(self.descriptors.mean_descriptors[i])):
                self.descriptors.mean_descriptors[i][j] = \
                    ((self.size - 1)*self.descriptors.mean_descriptors[i][j] +
                     new_descriptors.mean_descriptors[i][j])/self.size

    def _update_labels(self, label):
        self.concat_labels += label

    def update(self, obj):
        self._update_objects(obj)
        self._update_signal(obj.signal)
        self._update_descriptors(obj.descriptors)
        self._update_labels(obj.label)
        self.size += 1

    def _reset_concat_label(self, labels):
        self.concat_labels = labels

    def _reset_object(self, objects):
        self.objects = objects

    def _reset_concat_signal(self, signals):
        self.concat_signal = signals

    def _reset_descriptors(self, descriptors):
        self.descriptors.copy(descriptors)

    def reset(self, objects):
        labels = objects[0].label
        signals = objects[0].signal
        descriptors = Descriptors()
        descriptors.copy(objects[0].descriptors)
        for obj in objects[1:]:
            labels += obj.label
            signals.extend(obj.signal)
            for i in range(descriptors.nb_descriptors):
                descriptors.update(obj.descriptors.concat_descriptors[i], obj.descriptors.mean_descriptors[i])
        self._reset_concat_label(labels)
        self._reset_object(objects)
        self._reset_concat_signal(signals)
        self._reset_descriptors(descriptors)

    def _pop_concat_label(self):
        self.concat_labels = self.concat_labels[:-1]

    def _pop_concat_signal(self):
        nb = int(len(self.concat_signal)/self.size)
        self.concat_signal = self.concat_signal[:-nb]

    def _pop_object(self):
        self.objects.pop()

    def _pop_descriptors(self):
        if len(self.descriptors.concat_descriptors) != 0:
            if len(self.descriptors.concat_descriptors[0]) > 1:
                for i in range(self.descriptors.nb_descriptors):
                    for j in range(len(self.descriptors.mean_descriptors[i])):
                        self.descriptors.mean_descriptors[i][j] = \
                            self.descriptors.mean_descriptors[i][j] - \
                            self.descriptors.concat_descriptors[i][len(self.descriptors.concat_descriptors[i]) - 1][j]\
                            / len(self.descriptors.concat_descriptors[i])
            else:
                self.descriptors.mean_descriptors.pop()
            for i in range(self.descriptors.nb_descriptors):
                self.descriptors.concat_descriptors[i].pop()

    def pop(self):
        self._pop_concat_label()
        self._pop_concat_signal()
        self._pop_descriptors()
        self._pop_object()
        self.size = self.size - 1


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
        self.signal.extend(signal)

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

    # TODO: jcalandra 20/09/2021 update function obj_rep.update_signal()
    def update_signal(self, signal):
        self.signal = signal
        # mean_trajectory(self.signal, signal)

    def update_label(self, label):
        self.label = label

    def update_descriptors(self, descriptors):
        self.nb += 1
        for i in range(self.descriptors.nb_descriptors):
            '''for j in range(len(self.descriptors.concat_descriptors[i])):
                for k in range(len(self.descriptors.concat_descriptors[i][j])):
                    self.descriptors.concat_descriptors[i][j][k] = \
                        ((self.nb - 1)*self.descriptors.concat_descriptors[i][j][k] +
                         descriptors.concat_descriptors[i][j][k])/self.nb'''
            for j in range(len(self.descriptors.mean_descriptors[i])):
                self.descriptors.mean_descriptors[i][j] = \
                    ((self.nb - 1)*self.descriptors.mean_descriptors[i][j] + descriptors.mean_descriptors[i][j])/self.nb

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
        self.nb_descriptors = 1
        self.concat_descriptors = []
        self.mean_descriptors = []

    # TODO: @jcalandra 09/09/2021 Descriptors functions
    #  MAJ les fonctions pour la classe descripteurs.
    def init_concat_descriptors(self, descriptors):
        self.concat_descriptors.append([descriptors])

    def init_mean_descriptors(self, descriptors):
        self.mean_descriptors.append(descriptors)

    def init(self, concat_descriptors, mean_descriptors):
        self.init_concat_descriptors(concat_descriptors)
        self.init_mean_descriptors(mean_descriptors)

    def update_concat_descriptors(self, concat_descriptors):
        for i in range(self.nb_descriptors):
            for j in range(len(self.concat_descriptors[i])):
                self.concat_descriptors[i].append(concat_descriptors[i])

    def update_mean_descriptors(self, mean_descriptors):
        for i in range(self.nb_descriptors):
            for j in range(len(self.mean_descriptors[i])):
                self.mean_descriptors[i][j] = \
                    ((len(self.concat_descriptors[0]) - 1) * self.mean_descriptors[i][j] +
                     mean_descriptors[j]) / len(self.concat_descriptors[0])

    def get_empty_descriptors(self, nb_descriptors):
        for i in range(nb_descriptors):
            self.concat_descriptors.append([])
            self.mean_descriptors.append([])

    def update(self, concat_descriptors, mean_descriptors):
        self.update_concat_descriptors(concat_descriptors)
        self.update_mean_descriptors(mean_descriptors)

    def compute_concat_descriptors(self, signal):
        return

    def compute_mean_descriptors(self, signal):
        return

    def compute(self, signal):
        self.compute_concat_descriptors(signal)
        self.compute_mean_descriptors(signal)

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
