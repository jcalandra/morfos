import object_storage
import parameters as prm

global mmarkers

class Marker:
    """ markers in Audacity format"""
    def __init__(self):
        self.begin_marker = 0
        self.end_marker = 0
        self.label = ""
        self.level = 0

    def compute_marker(self, object):
        self.begin_marker = round((object["coordinates"]["x"] - object["coordinates"]["z"]) * 1000)
        self.end_marker = round((object["coordinates"]["x"]) * 1000)
        self.label += "L" + str(object["level"]) + "T" + str(self.begin_marker) + "M" + str(object["mat_num"]) + \
                      "L" + str(object["level"])  + "_"
        self.level = object["level"]

    def store_marker(self):
        global mmarkers
        marker = {"begin_marker" : self.begin_marker, "end_marker" : self.end_marker, "label" : self.label}
        mmarkers.append(marker)


def find_cursor(cursor, marker):
    global mmarkers
    while marker.begin_marker > mmarkers[cursor]["begin_marker"] and cursor < len( mmarkers):
        cursor += 1
    return cursor


def store_level(cursor, marker):
    global mmarkers
    mmarkers[cursor]["label"] += marker.label
    return 0

def markers_init():
    global mmarkers
    mmarkers = []
    return 0


def compute_markers(objects, lvl):
    markers_init()
    for level in range(lvl, len(objects)):
        cursor = 0
        for i in range(len(objects[level])):
            marker = Marker()
            marker.compute_marker(objects[level][i])
            if level == lvl :
                marker.store_marker()
            else:
                cursor = find_cursor(cursor, marker)
                store_level(cursor, marker)




def produce_file(objects, path_result):
    global mmarkers
    starting_lvl = 0
    compute_markers(objects, starting_lvl)
    file = open(path_result + "mikhail_markers.txt", "a")
    file.write("# onset(ms)\tend(ms)\tlabel\n")
    for m in mmarkers:
        file.write(str(m["begin_marker"]) + "\t" + str(m["end_marker"]) + "\t" + str(m["label"]) + "\n")
    file.close()
    print("file saved as " + path_result + "mikhail_markers.txt")
