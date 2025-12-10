import sys
from pathlib import Path
file = Path(__file__).resolve()

project_root = str(file.parents[0])
print("Project root path:", project_root)
src_path = project_root
sys.path.append(src_path)

core_path = src_path + '/core'
sys.path.append(core_path)

criterias_path = src_path + '/criterias'
sys.path.append(criterias_path)

others_path = src_path + '/others'
sys.path.append(others_path)

exp_path = src_path + '/exp'
sys.path.append(exp_path)

mod_ML_path = core_path + '/ML'
sys.path.append(mod_ML_path)

test_path = src_path + 'test'
sys.path.append(test_path)


mod_algorithms_path = core_path + '/module_algorithms'
mod_mso_path = core_path + '/module_mso'
mod_parameters_path = core_path + '/module_parameters'
mod_visualization_path = core_path + '/module_visualization'
sys.path.append(mod_algorithms_path)
sys.path.append(mod_mso_path)
sys.path.append(mod_parameters_path)
sys.path.append(mod_visualization_path)

mod_classification_path = criterias_path + '/module_classification'
mod_precomputing_path = criterias_path + '/module_precomputing'
mod_segmentation_path = criterias_path + '/module_segmentation'
sys.path.append(mod_classification_path)
sys.path.append(mod_precomputing_path)
sys.path.append(mod_segmentation_path)

mod_rwcpop_path = exp_path + '/rwcpop'
sys.path.append(mod_rwcpop_path)

mod_synthesis_path = others_path + '/synthesis'
mod_markers_path = others_path + '/markers'
sys.path.append(mod_synthesis_path)
sys.path.append(mod_markers_path)

mso_path = mod_mso_path + '/mso'
oracle_path = mso_path + '/oracle'
obj_model_path = mod_mso_path + '/object_model'
sys.path.append(mso_path)
sys.path.append(oracle_path)
sys.path.append(obj_model_path)