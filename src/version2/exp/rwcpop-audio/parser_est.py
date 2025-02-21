import sys
import numpy
from pathlib import Path

file = Path(__file__).resolve()
project_root = str(file.parents[2])
src_path = project_root
sys.path.append(src_path)

import numpy as np
import my_paths as my_paths
import segmentations
import class_main
import others.object_storage as obj_s

test_path = project_root + '/../../data/rwcpop/'
result_path = project_root + '/../../results/ismir2025/test1/'

def compute_fd(test_path_pop, result_path_pop):
        class_main.main(name=test_path_pop, format=".wav", path_sound=test_path, path_result=result_path_pop)
        segmentations.produce_file(obj_s.objects, result_path_pop)


def parse_est(pop_song, result_path):
    compute_fd(pop_song, result_path)
    est_intervals_all = []
    est_labels_all = []
    for level in range(len(obj_s.objects)):
        path = result_path + "ismir2025_segmentations_level"+ str(level) +".txt"
        est_interval = []
        est_label = []
        with open(path, "r", encoding="utf-8") as f:
            for interval in f:
                interval = interval.rstrip().split("\t")
                est_interval.append([int(interval[0]), int(interval[1])])
                est_label.append([interval[2]])
        est_interval = numpy.array(est_interval)
        est_intervals_all.append(est_interval)
        est_labels_all.append(est_label)
    print("est_labels_all = ", est_labels_all)
    print("est_intervals_all = ", est_intervals_all)
    return est_labels_all, est_intervals_all

def test():
    print("start")
    number = '01'
    print("project_root = ", project_root)
    pop_song = 'Pop ' + number
    result_path_pop = result_path + '/Pop ' + number +'/'
    est_labels_all, est_intervals_all = parse_est(pop_song, result_path_pop)
    print("est_labels_all = ", est_labels_all)
    print("est_intervals_all = ", est_intervals_all)

#test()
