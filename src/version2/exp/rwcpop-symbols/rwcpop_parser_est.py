import sys
from pathlib import Path

file = Path(__file__).resolve()
project_root = str(file.parents[2])
src_path = project_root
sys.path.append(src_path)

import numpy as np
import my_paths as my_paths
import rwcpop_parser
import class_main
import module_parameters.parameters as prm
import others.object_storage as obj_s

def rwcpop_compute_fd(test_path, result_path):
    print(test_path)
    print(result_path)
    pop_xx = rwcpop_parser.parser(test_path)
    print("pop_xx = ", pop_xx)
    class_main.main(name=[str(pop_xx), [],[],[]], format='.txt', path_result=result_path)


def rwcpop_parse_est(test_path, result_path):
    rwcpop_compute_fd(test_path, result_path)
    objs = obj_s.objects
    est_labels_all = []
    est_intervals_all = []
    for level in range(len(objs)):
        est_labels_all.append([])
        est_intervals_all.append(np.zeros((len(objs[level]), 2)))
        for j in range(len(objs[level])):
            est_labels_all[level].append(str(objs[level][j]["coordinates"]["y"]))
            if j == 0:
                last_timer = 0
            else:
                last_timer = objs[level][j - 1]["coordinates"]["x"]/2
            est_intervals_all[level][j, 0] = last_timer
            est_intervals_all[level][j, 1] = objs[level][j]["coordinates"]["x"]/2
    return est_labels_all, est_intervals_all

def test():
    print("start")
    number = '11'
    test_path = project_root + '/../../data/rwcpop/Pop ' + number + ' (grid).csv'
    result_path = project_root + '/../../results/exp_rwcpop/version2/Pop ' + number +'/'
    est_labels_all, est_intervals_all = rwcpop_parse_est(test_path, result_path)
    print("est_labels_all = ", est_labels_all)
    print("est_intervals_all = ", est_intervals_all)

#test()
