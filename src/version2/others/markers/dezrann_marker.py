import object_storage
import parameters as prm

global mmarkers

class Marker:
    """ markers in Dezrann format"""
    def __init__(self):
        self.level = 0
        self.materiau = ""
        self.begin_marker = 0
        self.duration = 0

    def compute_marker(self, object):
        self.level = object["level"]
        self.materiau += str(object["mat_num"]) 
        self.begin_marker = round((object["coordinates"]["x"] - object["coordinates"]["z"]) * 6) #* 1000)
        self.duration = round((object["coordinates"]["z"]) * 6) #* 1000)


    def store_marker(self):
        global mmarkers
        marker = { "level" : self.level, "materiau" : self.materiau, "begin_marker" : self.begin_marker, "duration" : self.duration}
        mmarkers.append(marker)


def store_level(cursor, marker):
    global mmarkers
    mmarkers[cursor]["materiau"] += marker.materiau
    return 0

def markers_init():
    global mmarkers
    mmarkers = []
    return 0


def compute_markers(objects, lvl):
    for i in range(len(objects[lvl])):
        marker = Marker()
        marker.compute_marker(objects[lvl][i])
        marker.store_marker()


def produce_file(objects, path_result):
    global mmarkers
    markers_init()
    starting_lvl = 0
    for level in range(starting_lvl,len(objects)):
        compute_markers(objects, level)
    file = open(path_result + "dezrann_markers.txt", "a")
    file.write("{\n \"labels\":[\n")
    for m in mmarkers:
        file.write("   {\"type\": \"level-" + str(m["level"]) + "\", \"tag\": \"" + str(m["materiau"]) + "\", \"start\": " + str(m["begin_marker"]) + "\", \"duration\": " + str(m["duration"])+ "},\n")
    file.write(" ]\n}")
    file.close()
    print("file saved as " + path_result + "dezrann_markers.txt")