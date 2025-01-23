from class_object import Descriptors, borders

class ConcatObj:
    def __init__(self):
        self.objects = []
        self.concat_signals = []
        self.concat_labels = ""
        self.descriptors = Descriptors()
        self.durations = 0
        self.size = 0

    def init(self, new_obj):
        self.objects = [new_obj]
        self.concat_signals = new_obj.signal
        self.concat_labels = new_obj.label
        self.descriptors.copy(new_obj.descriptors)
        self.durations = new_obj.duration
        self.size = 1

    def _update_objects(self, obj):
        self.objects.append(obj)

    def _update_signal(self, signal):
        self.concat_signals += signal

    def _update_labels(self, label):
        self.concat_labels += label

    def _update_descriptors(self, new_descriptors):
        for i in range(self.descriptors.nb_descriptors):
            """for j in range(len(new_descriptors.concat_descriptors[i])):
                self.descriptors.concat_descriptors[i].append(new_descriptors.concat_descriptors[i][j])"""
            for j in range(len(new_descriptors.mean_descriptors[i])):
                for k in range(len(new_descriptors.mean_descriptors[i][j])):
                    self.descriptors.mean_descriptors[i][j][k] = (self.descriptors.mean_descriptors[i][j][k]*self.size + new_descriptors.mean_descriptors[i][j][k])/(self.size+1)

    def update_duration(self, duration):
        self.durations += duration

    def update_size(self):
        self.size += 1

    def update(self, obj):
        self._update_objects(obj)
        self._update_signal(obj.signal)
        self._update_labels(obj.label)
        self._update_descriptors(obj.descriptors)
        self.update_duration(obj.duration)
        self.update_size()

    def _reset_object(self, objects):
        self.objects = objects

    def _reset_concat_signal(self, signals):
        self.concat_signal = signals

    def _reset_concat_label(self, labels):
        self.concat_labels = labels

    def _reset_descriptors(self, descriptors):
        self.descriptors.copy(descriptors)

    def _reset_durations(self, durations):
        self.durations = durations

    def reset(self, objects):
        signals = objects[0].signal
        labels = objects[0].label
        descriptors = Descriptors()
        descriptors.copy(objects[0].descriptors)
        durations = objects[0].duration
        for obj in objects[1:]:
            labels += obj.label
            signals.extend(obj.signal)
            for i in range(descriptors.nb_descriptors):
                descriptors.update(obj.descriptors.concat_descriptors[i], obj.descriptors.mean_descriptors[i])
            durations += obj.duration
        self._reset_object(objects)
        self._reset_concat_signal(signals)
        self._reset_concat_label(labels)
        self._reset_descriptors(descriptors)
        self._reset_durations(durations)
        self.size = len(labels)

    def _pop_concat_label(self):
        self.concat_labels = self.concat_labels[:-1]

    def _pop_concat_signal(self):
        nb = int(len(self.objects[-1].signal))
        self.concat_signal = self.concat_signal[:-nb]

    def _pop_object(self):
        self.objects.pop()

    def _pop_descriptors(self):
        if len(self.descriptors.concat_descriptors) != 0:
            if len(self.descriptors.concat_descriptors[0]) > 1:
                for i in range(self.descriptors.nb_descriptors):
                    for j in range(len(self.descriptors.mean_descriptors[i])):
                        if len(self.descriptors.concat_descriptors[i]) <= borders + 1:
                            self.descriptors.mean_descriptors[i][j] = self.descriptors.concat_descriptors[i][len(self.descriptors.concat_descriptors[i]) - 2][j]
                        else:
                            self.descriptors.mean_descriptors[i][j] = \
                                self.descriptors.mean_descriptors[i][j] - \
                                self.descriptors.concat_descriptors[i][len(self.descriptors.concat_descriptors[i]) - 1][j] \
                                / (len(self.descriptors.concat_descriptors[i]) - borders)
            else:
                if len(self.descriptors.mean_descriptors) > 0:
                    self.descriptors.mean_descriptors.pop()
            for i in range(self.descriptors.nb_descriptors):
                self.descriptors.concat_descriptors[i].pop()

    def _pop_duration(self):
        self.durations = self.durations - self.objects[-1].duration

    def _pop_size(self):
        self.size = self.size - 1

    def pop(self):
        self._pop_concat_label()
        self._pop_concat_signal()
        self._pop_descriptors()
        self._pop_duration()
        self._pop_object()
        self._pop_size()

    def copy(self, concatObj):
        self.objects = concatObj.objects
        self.concat_signal = concatObj.concat_signal
        self.concat_labels = concatObj.concat_labels
        self.descriptors = concatObj.descriptors
        self.durations = concatObj.durations
        self.size = concatObj.size

