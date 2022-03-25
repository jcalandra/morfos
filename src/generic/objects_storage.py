#info objects
global data
global objects
global first_occ

def data_init(local_data):
    global data
    data = local_data
    return 0

def objects_init():
    global objects
    objects = []
    return 0

def objects_add_new_obj(id, links, x, y, z, mat_num, level, sound):
    # id: identifier for the object at a specific level
    # links: identifier of the children
    # coordinates: x is the segmentation date of the object
    #              y is the date of first apparition of the corresponding material of the object
    #              z is the duration of the object
    # mat_num: identification number of the objects's corresponding material
    # level: level in with the object belongs (might be useful for the choice of the color in the representation)
    # sound: digitised data corresponding to the sound associated to the object
    global objects
    object = {"id": id, "links": links, "coordinates": {"x":x, "y": y, "z":z}, "mat_num": mat_num ,"level":level,
              "sound": sound}
    objects[level].append(object)
    return 0

def objects_modify_prev_obj(level, mat_num_prev1, mat_num_prev2, y_prev1, y_prev2):
    global objects
    objects[level][len(objects[level]) - 2]["mat_num"] = mat_num_prev1
    objects[level][len(objects[level]) - 3]["mat_num"] = mat_num_prev2
    objects[level][len(objects[level]) - 2]["coordinates"]["y"] = y_prev1
    objects[level][len(objects[level]) - 3]["coordinates"]["y"] = y_prev2
    return 0

def objects_add_level():
    global objects
    objects.append([])
    return 0

def first_occ_init():
    global first_occ
    first_occ = []
    return 0

def first_occ_add_level():
    global first_occ
    first_occ.append([])
    return 0

def first_occ_add_obj(level, y):
    global first_occ
    first_occ[level].append(y)
    return 0

def first_occ_remove_obj(level):
    global first_occ
    first_occ[level].pop()
    return 0
