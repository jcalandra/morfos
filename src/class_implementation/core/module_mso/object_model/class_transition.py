from object_model import class_object as co


class Transition:
    def __init__(self):
        self.prev_obj = None
        self.next_obj = None

        self.transit_signal = []
        self.transit_descriptors = co.Descriptors()
        self.transit_label = ""
        self.transit_functions = co.TransFunctions()
        self.transit_rep = TransitRep()

    def update_objs(self, prev_obj, next_obj):
        self.prev_obj = prev_obj
        self.next_obj = next_obj

    def update_transit_signal(self, signal):
        return

    def update_transit_descriptors(self, descriptors):
        return

    def update_transit_label(self, label):
        return

    def update_transit_functions(self, functions):
        return

    def update_transit_rep(self, rep):
        self.transit_rep.copy(rep)
        rep.update(self.transit_signal, self.transit_label, self.transit_descriptors)

    def update(self, prev_obj, next_obj, descriptors, label, functions, rep):
        self.update_objs(prev_obj, next_obj)
        self.update_transit_descriptors(descriptors)
        self.update_transit_label(label)
        self.update_transit_functions(functions)
        self.update_transit_rep(rep)

    def copy(self, transit):
        self.prev_obj.copy(transit.prev_obj)
        self.next_obj.copy(transit.next_obj)
        self.transit_signal = transit.transit_signal
        self.transit_label = transit.transit_label
        self.transit_descriptors.copy(transit.transit_descriptors)
        self.transit_functions = transit.transit_functions
        self.transit_rep.copy(transit.transit_rep)


# TODO: @jcalandra 09/09/2021
#  On constate que les classes ObjRep et TransitRep sont exactement les mêmes
#  Il faut faire une classe générique qui contient les deux
class TransitRep:
    def __init__(self):
        self.transit_signal = []
        self.transit_label = ""
        self.transit_descriptors = co.Descriptors()
        self.nb = 0

    def init_transit_signal(self, signal):
        self.transit_signal += signal

    def init_transit_label(self, label):
        self.transit_label += label

    def init_transit_descriptors(self, descriptors):
        self.transit_descriptors.copy(descriptors)

    def init_transit_nb(self):
        self.nb = 1

    def init(self, signal, label, descriptors):
        self.init_transit_signal(signal)
        self.init_transit_label(label)
        self.init_transit_descriptors(descriptors)
        self.init_transit_nb()

    def update_transit_signal(self, signal):
        co.mean_trajectory(self.transit_signal, signal)

    def update_transit_label(self, label):
        self.label = label

    def update_transit_descriptors(self, descriptors):
        self.nb += 1
        for i in len(self.transit_descriptors.concat_descriptors):
            self.transit_descriptors.concat_descriptors[i] = \
                ((self.nb - 1)*self.transit_descriptors.concat_descriptors[i] + descriptors.concat_descriptors[i])/self.nb
        for i in len(self.transit_descriptors.mean_descriptors):
            self.transit_descriptors.mean_descriptors[i] = \
                ((self.nb - 1)*self.transit_descriptors.mean_descriptors[i] + descriptors.mean_descriptors[i])/self.nb

    def update(self, signal, label, descriptors):
        self.update_transit_signal(signal)
        self.update_transit_label(label)
        self.update_transit_descriptors(descriptors)

    def copy(self, rep):
        self.transit_signal = rep.transit_signal
        self.transit_label = rep.transit_label
        self.transit_descriptors.copy (rep.transit_descriptors)
        self.nb = rep.nb
