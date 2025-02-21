import sys
from pathlib import Path

file = Path(__file__).resolve()
project_root = str(file.parents[2])
src_path = project_root
sys.path.append(src_path)

import my_paths as my_paths
import class_main
import others.object_storage as obj_s
import segmentations

test_path = project_root + '/../../data/rwcpop/'
result_path = project_root + '/../../results/ismir2025/test1/'


def compute_fd_all():
    for i in range(1,101):
        if i < 10:
            number = '0' + str(i)
        else:
            number = str(i)
        test_path_pop = 'Pop ' + number
        result_path_pop = result_path + '/Pop ' + number + '/'
        print(test_path_pop)
        class_main.main(name=test_path_pop, format=".wav", path_sound=test_path, path_result=result_path_pop)
        segmentations.produce_file(obj_s.objects, result_path_pop)


#compute_fd_all()