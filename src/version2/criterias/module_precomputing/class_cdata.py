class Elements:
    """
    Element data. Principal data depending on the type of input data.
    It contains the audio, the symbol and the pitch.
    """
    def __init__(self):
        self.audio = None
        self.symbol = None
        self.pitch = None

        # setters
    def set_audio(self, audio):
        self.audio = audio
    def set_symbol(self, symbol):   
        self.symbol = symbol
    def set_pitch(self, pitch):
        self.pitch = pitch
    def set_elements(self, audio, symbol, pitch):
        self.audio = audio
        self.symbol = symbol
        self.pitch = pitch

        # getters
    def get_audio(self):
        return self.audio
    def get_symbol(self):
        return self.symbol
    def get_pitch(self):
        return self.pitch

        # printing
    def print(self):    
        print("audio", self.audio)
        print("symbol", self.symbol)
        print("pitch", self.pitch)

        # reset
    def reset(self):   
        self.audio = None
        self.symbol = None
        self.pitch = None
    

class ParsedElement:
    """
    Parsed input data. Contains the elements (audio, symbol, pitch), the velocity, the date, the duration, 
    the descriptors, each in tabs and the common length of the tabs.
    It is used to store the data of the input data.
    """
    def __init__(self):
        self.elements = Elements()
        self.velocity = None
        self.date = None
        self.duration = None
        self.descriptors = None
        self.length = 0


        # setters
    def set_elements(self, elements):
        self.elements = elements
    def set_velocity(self, velocity):
        self.velocity = velocity
    def set_date(self, date):
        self.date = date
    def set_duration(self, duration):
        self.duration = duration
    def set_descriptors(self, descriptors):
        self.descriptors = descriptors
    def set_length(self, length):
        self.length = length

        # getters
    def get_elements(self):
        return self.elements
    def get_velocity(self):
        return self.velocity
    def get_date(self):
        return self.date
    def get_duration(self):
        return self.duration
    def get_descriptors(self):
        return self.descriptors
    def get_length(self):
        return self.length

        # printing
    def print(self):
        self.elements.print()
        print("velocity", self.velocity)
        print("date", self.date)
        print("duration", self.duration)
        print("descriptors", self.descriptors)
        print("length", self.length)

        # reset 
        
    def reset(self):   
        self.elements = Elements()
        self.velocity = None
        self.date = None
        self.duration = None
        self.descriptors = None
        self.length = 0


class CData:
    """
    Computed data.
    """
    def __init__(self):
        self.input_data = ParsedElement()
        self.dim = None
        self.type = None

        # setters
    def set_input_data(self, input_data):
        self.input_data = input_data
    def set_dim(self, dim):
        self.dim = dim
    def set_type(self, type):   
        self.type = type

        # getters
    def get_input_data(self):
        return self.input_data
    def get_dim(self):
        return self.dim
    def get_type(self):
        return self.type

        # printing
    def print(self):
        self.input_data.print()
        print("dim", self.dim)
        print("type", self.type)

        # reset
    def reset(self):
        self.input_data = ParsedElement()
        self.dim = None
        self.type = None