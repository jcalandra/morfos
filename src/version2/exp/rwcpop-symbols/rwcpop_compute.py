import rwcpop_parser_ref as rwcpp_ref
import rwcpop_parser_est as rwcpp_est
import module_parameters.parameters as prm

test_path = rwcpp_est.project_root + '/../../data/rwcpop'
result_path = rwcpp_est.project_root + '/../../results/exp_rwcpop/version2/fmes3_120bpm/test6/analysis/'

def rwcpop_compute_fd_all():
    for i in range(21,22):
        if i < 10:
            number = '0' + str(i)
        else:
            number = str(i)
        test_path_pop = test_path + '/Pop ' + number + ' (grid).csv'
        result_path_pop = result_path + '/Pop ' + number + '/'
        rwcpp_est.rwcpop_compute_fd(test_path_pop, result_path_pop)


rwcpop_compute_fd_all()