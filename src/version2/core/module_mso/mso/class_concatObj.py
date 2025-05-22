from class_object import Descriptors, borders


class ConcatObj:
    def __init__(self):
        self.objects = []
        self.extConcatNote = extConcatNote()
        self.nb = 0

    def init(self, new_obj):
        self.objects = [new_obj]
        self.extConcatNote.init(new_obj)
        self.nb = 1

# setters
    def set_objects(self, objects): 
        self.objects = objects
    def set_extConcatNote(self, extConcatNote):
        self.extConcatNote = extConcatNote
    def set_nb(self, nb):
        self.nb = nb

# getters
    def get_objects(self):
        return self.objects
    def get_extConcatNote(self):
        return self.extConcatNote
    def get_nb(self):
        return self.nb

# update
    def _update_objects(self, obj):
        self.objects.append(obj)

    def _update_extConcatNote(self, obj, concatobj):
        self.extConcatNote.update(obj, concatobj)

    def _update_nb(self):
        self.nb += 1

    def update(self, obj):
        self._update_objects(obj)
        self._update_extConcatNote(obj, self)
        self._update_nb()

# reset
    def _reset_object(self, objects):
        self.objects = objects

    def _reset_extConcatNote(self, new_obj):
        self.extConcatNote.reset(new_obj)
    
    def _reset_nb(self, nb):
        self.nb = nb



    def reset(self, objects):
        new_obj = objects[0]
        self.extConcatNote.reset(new_obj)
        date = objects[0].date
        durations = objects[0].duration
        for obj in objects[1:]:
            self.extConcatNote.concatNote.update(obj)
            durations += obj.duration
        self.extConcatNote.durations = durations
        self.extConcatNote.date = date
        self._reset_object(objects)
        self._reset_nb(len(objects))

# pop

    def _pop_object(self):
        self.objects.pop()

    def _pop_extConcatNote(self):
        self.extConcatNote.pop()

    def _pop_nb(self):
        self.nb = self.nb - 1

    def pop(self):
        self._pop_object()
        self._pop_extConcatNote(self)
        self._pop_nb()

    def copy(self, concatObj):
        self.objects = concatObj.objects
        self.extConcatNote.copy(concatObj.extConcatNote)
        self.nb = concatObj.nb


class extConcatNote:
    def __init__(self):
        self.concatNote = concatNote()
        self.durations = 0
        self.date = 0

    def init(self, new_obj):
        self.concatNote.init(new_obj)
        self.durations = new_obj.extNotes[0].duration
        self.date = new_obj.extNotes[0].date

# setters
    def set_concatNote(self, concatNote):
        self.concatNote = concatNote
    def set_durations(self, durations):
        self.durations = durations
    def set_date(self, date):
        self.date = date


# getters
    def get_concatNote(self):
        return self.concatNote
    def get_durations(self):
        return self.durations
    def get_date(self):
        return self.date

# update
    def _update_concatNote(self, obj, concatobj):
        self.concatNote.update(obj, concatobj)
    def _update_durations(self, duration):
        self.durations += duration
    def _update_date(self, date):
        pass

    def update(self, obj, concatobj):
        self._update_concatNote(obj, concatobj)
        self._update_durations(obj.extNotes[0].duration)
        self._update_date(obj.extNotes[0].date)

# reset
    def _reset_concatNote(self, new_obj):
        self.concatNote.reset(new_obj)
    def _reset_durations(self, durations):
        self.durations = durations
    def _reset_date(self, date):
        self.date = date
    
    def reset(self, new_obj):
        self._reset_concatNote(new_obj)
        self._reset_durations(new_obj.duration)
        self._reset_date(new_obj.date)

# pop
    def _pop_concatNote(self):
        self.concatNote.pop()
    def _pop_durations(self):
        self.durations = self.durations - ConcatObj.objects[-1].duration
    def _pop_date(self):
        pass

    def pop(self, concatobj):
        self._pop_concatNote(concatobj)
        self._pop_durations()
        self._pop_date()

    def copy(self, extConcatNote):
        self.concatNote.copy(extConcatNote.concatNote)
        self.durations = extConcatNote.durations
        self.date = extConcatNote.date

class concatNote:
    def __init__(self):
        self.concat_audio = []
        self.concat_labels = ""
        self.concat_pitches = []
        self.descriptors = Descriptors()
        self.concat_velocity = []

    def init(self, new_obj):
        self.concat_audio = new_obj.extNotes[0].note.audio
        self.concat_labels = new_obj.extNotes[0].note.label
        self.concat_pitches = new_obj.extNotes[0].note.pitch
        self.descriptors.copy(new_obj.extNotes[0].note.descriptors)
        self.concat_velocity = new_obj.extNotes[0].note.velocity

# setters
    def set_concat_audio(self, audio):
        self.concat_audio = audio
    def set_concat_label(self, labels):
        self.concat_labels = labels
    def set_concat_pitches(self, pitches):
        self.concat_pitches = pitches
    def set_descriptors(self, descriptors):
        self.descriptors = descriptors
    def set_concat_velocity(self, velocity):
        self.concat_velocity = velocity

# getters
    def get_concat_audio(self):
        return self.concat_audio
    def get_concat_label(self):
        return self.concat_labels
    def get_concat_pitches(self):
        return self.concat_pitches
    def get_descriptors(self):
        return self.descriptors
    def get_concat_velocity(self):
        return self.concat_velocity

# update
    def _update_audio(self, audio):
        self.concat_audio += audio

    def _update_labels(self, label):
        self.concat_labels += label

    def _update_pitches(self, pitch):
        self.concat_pitches += pitch

    def _update_descriptors(self, new_descriptors, concatobj):
        
        #for i in range(descriptors.nb_descriptors):
           #descriptors.update(obj.extNotes[0].note.descriptors.concat_descriptors[i], obj.extNotes[0].note.descriptors.mean_descriptors[i])

        for i in range(self.descriptors.nb_descriptors):
            self.descriptors.concat_descriptors[i].extend(new_descriptors.concat_descriptors[i])
            for j in range(len(new_descriptors.mean_descriptors[i])):
                for k in range(len(new_descriptors.mean_descriptors[i][j])):
                    self.descriptors.mean_descriptors[i][j][k] = (self.descriptors.mean_descriptors[i][j][k]*concatobj.nb + new_descriptors.mean_descriptors[i][j][k])/(concatobj.nb+1)


    def _update_velocity(self, velocity):
        self.concat_velocity += velocity

    def update(self, new_obj, concatobj):
        self._update_audio(new_obj.extNotes[0].note.audio)
        self._update_labels(new_obj.extNotes[0].note.label)
        self._update_pitches(new_obj.extNotes[0].note.pitch)
        self._update_descriptors(new_obj.extNotes[0].note.descriptors, concatobj)
        self._update_velocity(new_obj.extNotes[0].note.velocity)

# reset
    def _reset_concat_audio(self, audio):
        self.concat_audio = audio

    def _reset_concat_label(self, labels):
        self.concat_labels = labels

    def _reset_concat_pitch(self, pitches):
        self.concat_pitches = pitches

    def _reset_descriptors(self, descriptors):
        self.descriptors.copy(descriptors)

    def _reset_concat_velocity(self, velocity):
        self.concat_velocity = velocity

    
    def reset(self, new_obj):
        self._reset_concat_audio(new_obj.extNotes[0].note.audio)
        self._reset_concat_label(new_obj.extNotes[0].note.label)
        self._reset_concat_pitch(new_obj.extNotes[0].note.pitch)
        self._reset_descriptors(new_obj.extNotes[0].note.descriptors)
        self._reset_concat_velocity(new_obj.extNotes[0].note.velocity)

# pop
    def _pop_concat_audio(self, concatobj):
        size = int(len(concatobj.objects[-1].extNotes[0].note.audio))
        self.concat_audio = self.concat_audio[:-size]

    def _pop_concat_label(self):
        self.concat_labels = self.concat_labels[:-1]
    
    def _pop_concat_pitch(self):
        self.concat_pitches = self.concat_pitches[:-1]

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

    def _pop_concat_velocity(self):
        self.concat_velocity = self.concat_velocity[:-1]


    def pop(self, concatobj):
        self._pop_concat_audio(concatobj)
        self._pop_concat_label()
        self._pop_concat_pitch()
        self._pop_descriptors()

    def copy(self, concatNote):
        self.concat_audio = concatNote.concat_audio
        self.concat_labels = concatNote.concat_labels
        self.concat_pitches = concatNote.concat_pitches
        self.concat_descriptors.copy(concatNote.concat_descriptors)
        self.concat_velocity = concatNote.concat_velocity
