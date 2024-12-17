borders = 3


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
                for k in range(len(self.descriptors.mean_descriptors[i][j])):
                    if self.nb <= borders + 1:
                        self.descriptors.mean_descriptors[i][j][k] = descriptors.mean_descriptors[i][j][k]
                    else:
                        self.descriptors.mean_descriptors[i][j][k] = \
                            ((self.nb - borders - 1)*self.descriptors.mean_descriptors[i][j][k] + descriptors.mean_descriptors[i][j][k]) / \
                            (self.nb - borders)

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
        self.nb_descriptors = 0
        self.concat_descriptors = []
        self.mean_descriptors = []

    # TODO: @jcalandra 09/09/2021 Descriptors functions
    #  MAJ les fonctions pour la classe descripteurs.
    def init_concat_descriptors(self, descriptors):
        self.concat_descriptors = descriptors

    def init_mean_descriptors(self, descriptors):
        self.mean_descriptors = descriptors

    def init(self, concat_descriptors, mean_descriptors):
        self.init_concat_descriptors(concat_descriptors)
        self.init_mean_descriptors(mean_descriptors)
        self.nb_descriptors += 1

    def update_concat_descriptors(self, concat_descriptors):

        for i in range(self.concat_descriptors):
            for j in range(len(self.concat_descriptors[i])):
                self.concat_descriptors[i].append(concat_descriptors[i])

    def update_mean_descriptors(self, mean_descriptors):
        for i in range(self.mean_descriptors):
            for j in range(len(self.mean_descriptors[i])):
                if len(self.concat_descriptors[0]) <= borders + 1:
                    self.mean_descriptors[i][j] = mean_descriptors[j]
                else:
                    self.mean_descriptors[i][j] = \
                        ((len(self.concat_descriptors[0]) - 1) * self.mean_descriptors[i][j] +
                         mean_descriptors[j]) / (len(self.concat_descriptors[0]) - borders)

    def get_empty_descriptors(self, nb_descriptors):
        for i in range(nb_descriptors):
            self.concat_descriptors.append([])
            self.mean_descriptors.append([])

    def update(self, descriptors):
        self.update_concat_descriptors(descriptors.concat_descriptors)
        self.update_mean_descriptors(descriptors.mean_descriptors)

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
        self.nb_descriptors = descriptors.nb_descriptors


class TransFunctions:
    def __init__(self):
        self.label_functions = []
        self.descriptor_functions = []

    # TODO: @jcalandra 09/09/2021 Transformation functions
    #  MAJ les fonctions pour la classe des fonctions de transformation.
    def get_functions(self):
        return

