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
        self.begin_marker = round((object["coordinates"]["x"] - object["coordinates"]["z"]) * 100)
        self.end_marker = round((object["coordinates"]["x"]) * 100)
        self.label = "M" + str(object["mat_num"])
        self.level = object["level"]

    def store_marker(self):
        global mmarkers
        if self.level > len(mmarkers) - 1:
            mmarkers.append([])
        mmarkers[self.level].append({"begin_marker" : self.begin_marker, "end_marker" : self.end_marker, "label" : self.label})


def markers_init():
    global mmarkers
    mmarkers = []
    return 0


def compute_markers(objects):
    markers_init()
    for level in range(0, len(objects)):
        for i in range(len(objects[level])):
            marker = Marker()
            marker.compute_marker(objects[level][i])
            marker.store_marker()




def produce_file(objects, path_result):
    global mmarkers
    compute_markers(objects)
    for level in range(0, len(mmarkers)):
        file = open(path_result + "ismir2025_segmentations_level"+ str(level) +".txt", "w")
        for m in mmarkers[level]:
            file.write(str(m["begin_marker"]) + "\t" + str(m["end_marker"]) + "\t" + str(m["label"]) + "\n")
        file.close()
    print("file saved as " + path_result + "ismir2025_segmentations_level"+ str(level) +".txt")
