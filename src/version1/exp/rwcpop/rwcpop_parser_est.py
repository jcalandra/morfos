import main_mso_char
import numpy as np

file = main_mso_char.Path(__file__).resolve()
project_root = str(file.parents[2])


def rwcpop_compute_fd(test_path, result_path):
    pop_xx = main_mso_char.parser(test_path)
    main_mso_char.main(pop_xx, result_path)


def rwcpop_parse_est(test_path, result_path):
    rwcpop_compute_fd(test_path, result_path)
    objs = main_mso_char.obj_s.objects
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
    number = '01'
    test_path = project_root + '/../../data/rwcpop/Pop ' + number + ' (grid).csv'
    result_path = project_root + '/../../results/rwcpop/Pop ' + number +'/'
    est_labels_all, est_intervals_all = rwcpop_parse_est(test_path, result_path)
    print("est_labels_all = ", est_labels_all)
    print("est_intervals_all = ", est_intervals_all)
