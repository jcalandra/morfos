borders = 3


class Object:
    def __init__(self):
        self.id = None
        self.signal = []
        self.label = ""
        self.pitch = []
        self.descriptors = Descriptors()
        self.duration = 0
        self.date = 0
        self.transfo_functions = TransFunctions()
        self.obj_rep = ObjRep()

    def get_id(self, ind):
        self.id = ind

    def get_signal(self, signal):
        self.signal = signal

    def get_label(self, label):
        self.label = label

    def get_pitch(self, pitch):
        self.pitch = pitch

    def get_descriptors(self, descriptors):
        self.descriptors.copy(descriptors)

    def get_duration(self, duration):
        self.duration = duration

    def get_date(self, date):
        self.date = date

    def get_rep(self, rep):
        self.obj_rep.copy(rep)
        # rep.update(self.signal, self.label, self.descriptors)

    def get_similarity(self):
        return

    def update(self, signal, label, pitch, descriptors,  duration, date, rep):
        self.get_signal(signal)
        self.get_label(label)
        self.get_pitch(pitch)
        self.get_descriptors(descriptors)
        self.get_duration(duration)
        self.get_date(date)
        self.transfo_functions.get_functions()
        self.get_rep(rep)

    def copy(self, obj):
        self.id = obj.id
        self.signal = obj.signal
        self.label = obj.label
        self.pitch = obj.pitch
        self.descriptors.copy(obj.descriptors)
        self.duration = obj.duration
        self.date = obj.date
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
        self.pitch = []
        self.descriptors = Descriptors()
        self.duration = 0
        self.first_date = 0
        self.nb = 0

    def init_signal(self, signal):
        self.signal.extend(signal)

    def init_label(self, label):
        self.label += label

    def init_pitch(self, pitch):
        self.pitch.extend(pitch)

    def init_descriptors(self, descriptors):
        self.descriptors.copy(descriptors)

    def init_duration(self, duration):
        self.duration = duration

    def init_first_date(self, date):
        self.first_date = date

    def init_nb(self):
        self.nb = 1

    def init(self, signal, label, pitch, descriptors, duration, date):
        self.init_signal(signal)
        self.init_label(label)
        self.init_pitch(pitch)
        self.init_descriptors(descriptors)
        self.init_duration(duration)
        self.init_first_date(date)
        self.init_nb()

    # TODO: jcalandra 20/09/2021 update function obj_rep.update_signal()
    def update_signal(self, signal):
        self.signal = signal
        # mean_trajectory(self.signal, signal)

    def update_label(self, label):
        self.label = label

    def update_pitch(self, pitch):
        self.pitch = pitch

    def update_concat_descriptors(self, concat_descriptors):
        for i in range(self.descriptors.nb_descriptors):
            self.descriptors.concat_descriptors[i].extend(concat_descriptors[i])

    def update_mean_descriptors(self, mean_descriptors):
        new_mean_descriptor = []
        for i in range(self.descriptors.nb_descriptors):
            new_mean_descriptor.append([])
            new_mean_descriptor[i].append([0 for _ in range(len(mean_descriptors[i][0]))])
            for j in range(len(mean_descriptors[i])):
                    for k in range(len(mean_descriptors[i][j])):
                        if self.nb <= borders:
                            self.descriptors.mean_descriptors[i][0][k] = mean_descriptors[i][j][k]/len(mean_descriptors[0])
                        else:
                            self.descriptors.mean_descriptors[i][0][k] += mean_descriptors[i][j][k]/(len(mean_descriptors[0])*2)
                        
    def update_descriptors(self, descriptors):
        self.update_concat_descriptors(descriptors.concat_descriptors)
        self.update_mean_descriptors(descriptors.mean_descriptors)
                        
    def update_duration(self, duration):
        self.duration = (self.nb * self.duration + duration)/(self.nb + 1)

    def update_first_date(self, date):        
        pass

    def update_nb(self):
        self.nb += 1

    def update(self, signal, label, pitch, descriptors, duration, date):
        self.update_signal(signal)
        self.update_label(label)
        self.update_pitch(pitch)
        self.update_descriptors(descriptors)
        self.update_duration(duration)
        self.update_first_date(date)
        self.update_nb()

    def copy(self, rep):
        self.signal = rep.signal
        self.label = rep.label
        self.pitch = rep.pitch
        self.descriptors.copy(rep.descriptors)
        self.duration = rep.duration
        self.first_date = rep.first_date
        self.nb = rep.nb


class Descriptors:
    def __init__(self):
        self.nb_descriptors = 0
        self.concat_descriptors = []
        self.mean_descriptors = []

    def init_nb_descriptors(self):
        self.nb_descriptors = 1

    def init_concat_descriptors(self, descriptors):
        self.concat_descriptors = descriptors

    def init_mean_descriptors(self, descriptors):
        self.mean_descriptors = descriptors

    def init(self, concat_descriptors, mean_descriptors):
        self.init_concat_descriptors(concat_descriptors)
        self.init_mean_descriptors(mean_descriptors)
        self.init_nb_descriptors()


    def update_concat_descriptors(self, concat_descriptors):
        for i in range(self.descriptors.nb_descriptors):
            self.descriptors.concat_descriptors[i].extend(concat_descriptors[i])
        

    def update_mean_descriptors(self, mean_descriptors):
        for i in range(self.descriptors.nb_descriptors):
            for j in range(len(self.descriptors.mean_descriptors[i])):
                for k in range(len(self.descriptors.mean_descriptors[i][j])):
                    if self.nb <= borders:
                        self.descriptors.mean_descriptors[i][j][k] = mean_descriptors[i][j][k]
                    else:
                        self.descriptors.mean_descriptors[i][j][k] = \
                            ((self.nb - borders)*self.descriptors.mean_descriptors[i][j][k] + mean_descriptors[i][j][k]) / \
                            (self.nb - borders + 1)
        

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

