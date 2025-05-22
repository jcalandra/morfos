borders = 3

class Object:
    def __init__(self):
        self.id = None
        self.extNotes = []
        self.transfo_functions = TransFunctions()
        self.obj_rep = ObjRep()

# setters
    def set_id(self, ind):
        self.id = ind
    def set_extNotes(self, extNotes):
        self.extNotes = extNotes
    def set_transfo_functions(self, transfo_functions):
        self.transfo_functions = transfo_functions
    def set_obj_rep(self, obj_rep):
        self.obj_rep.copy(obj_rep)

# getters
    def get_id(self):
        return self.id
    def get_extNotes(self):
        return self.extNotes
    def get_transfo_functions(self):
        return self.transfo_functions
    def get_obj_rep(self):
        return self.obj_rep
    
# others
    def get_similarity(self):
        return

    def copy(self, obj):
        self.id = obj.id
        self.extNotes.copy(obj.extNotes)
        self.transfo_functions = obj.transfo_functions
        self.obj_rep.copy(obj.rep)

    def update(self, signal, label, pitch, descriptors,  duration, date, rep):
        extNote = ExtendedNote()
        extNote.update(signal, label, pitch, descriptors, 0, date, duration)
        extNotes = [extNote]
        self.set_id(0)
        self.set_extNotes(extNotes)
        self.transfo_functions.get_functions()
        self.set_obj_rep(rep)

# printing
    def print(self):
        print("id", self.id)
        print("extNotes")
        for extNote in self.extNotes:
            extNote.print()
        print("transfo_functions", self.transfo_functions)
        print("obj_rep", self.obj_rep)

   
# TODO: @jcalandra 09/09/2021 trajectoire moyenne
#  Définir la "trajectoire audio" moyenne à partir de la DTW
def mean_trajectory(signal_rep, signal):
    return

class ExtendedNote:
    def __init__(self):
        self.note = Note()
        self.date = 0
        self.duration = 0

# setters
    def set_note(self, note):
        self.note = note
    def set_date(self, date):
        self.date = date
    def set_duration(self, duration):
        self.duration = duration
# getters
    def get_note(self):
        return self.note
    def get_date(self):
        return self.date
    def get_duration(self):
        return self.duration
    
# others
    def copy(self, extNote):
        self.note.copy(extNote.note)
        self.date = extNote.date
        self.duration = extNote.duration

    def update(self, signal, label, pitch, descriptors, velocity, date, duration):
        self.note.update(signal, label, pitch, descriptors, velocity)
        self.date = date
        self.duration = duration

# printing
    def print(self):   
        self.note.print()
        print("date", self.date)
        print("duration", self.duration)

class Note:

    def __init__(self):
        self.audio = []
        self.label = ""
        self.pitch = 0
        self.descriptors = Descriptors()
        self.velocity = 0

# setters
    def set_audio(self, audio):
        self.audio = audio
    def set_label(self, label):
        self.label = label
    def set_pitch(self, pitch): 
        self.pitch = pitch
    def set_descriptors(self, descriptors):
        self.descriptors.copy(descriptors)
    def set_velocity(self, velocity):
        self.velocity = velocity
# getters
    def get_audio(self):
        return self.audio
    def get_label(self):
        return self.label
    def get_pitch(self):
        return self.pitch
    def get_descriptors(self):
        return self.descriptors
    def get_velocity(self):
        return self.velocity

#others
    def copy(self, note):
        self.audio = note.audio
        self.label = note.label
        self.pitch = note.pitch
        self.descriptors.copy(note.descriptors)
        self.velocity = note.velocity

    def update(self, signal, label, pitch, descriptors, velocity):
        self.audio = signal
        self.label = label
        self.pitch = pitch
        self.descriptors.copy(descriptors)
        self.velocity = velocity

# printing
    def print(self):
        print("audio", self.audio)
        print("label", self.label)
        print("pitch", self.pitch)
        print("descriptors", self.descriptors)
        print("velocity", self.velocity)
        
## OBJ REP

class ObjRep:
    def __init__(self):
        self.extNotesRep = [] #tab of ExtendedNoteRep()
        self.nb = 0

    def init_nb(self):
        self.nb = 1

    def init(self, signal, label, pitch, descriptors, duration, date):
        extnote_rep = ExtendedNoteRep()
        extnote_rep.init(signal, label, pitch, descriptors, 0, date, duration)
        self.extNotesRep.append(extnote_rep)
        self.init_nb()

    def update_nb(self):
        self.nb += 1

    def update(self, signal, label, pitch, descriptors, duration, date):
        extendednoterep = ExtendedNoteRep()
        extendednoterep.init(signal, label, pitch, descriptors, 0, date, duration)
        self.extNotesRep.append(extendednoterep)
        self.update_nb()

    def copy(self, rep):
        self.extNotesRep = rep.extNotesRep
        self.nb = rep.nb


class ExtendedNoteRep:
    def __init__(self):
        self.note = Note()
        self.first_date = 0
        self.mean_duration = 0

    def init(self, signal, label, pitch, descriptors, velocity, first_date, mean_duration):
        self.note.update(signal, label, pitch, descriptors, velocity)
        self.first_date = first_date
        self.mean_duration = mean_duration

# setters
    def set_notes(self, note):
        self.note.copy(note)
    def set_firs_date(self, first_date):
        self.first_date = first_date
    def set_mean_duration(self, mean_duration):
        self.mean_duration = mean_duration
# getters
    def get_notes(self):
        return self.note
    def get_first_date(self):
        return self.first_date
    def get_mean_duration(self):
        return self.mean_duration
    
# others
    def copy(self, extNotesRep):
        self.note.copy(extNotesRep.note)
        self.first_date = extNotesRep.first_date
        self.mean_duration = extNotesRep.mean_duration

    def update_mean_duration(self, mean_duration):
        self.mean_duration = (super.nb * self.mean_duration + mean_duration)/(super.nb + 1)

    def update(self, signal, label, pitch, descriptors, velocity, first_date, mean_duration):
        note = Note()
        self.note.update(signal, label, pitch, descriptors, velocity)
        self.notes.append(note)
        self.first_date = first_date
        self.mean_duration = mean_duration

# printing
    def print(self):   
        print("notes")
        for note in self.notes:
            note.print()
        print("first_date", self.first_date)
        print("mean_duration", self.mean_duration)
      
## DESCRIPTORS

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
