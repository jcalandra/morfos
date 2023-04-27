import data_processing as dp
from structure_measures import compute_segs_accuracy
from cogload_measures import *

def process_data(raw_data, path):
    # DATA PROCESSING
    data = dp.process_data(raw_data, path)
    return data


def process_ref():
    ref_segs = dp.process_segs()
    return ref_segs


def compute_data(data, group):
    # SEGMENTATION ANALYSIS
    segs_songs = segs_per_song(data)
    # NASA ANALYSIS
    nasas = nasatlx_per_subject(data)
    nasa_result = nasaresult_per_subject(nasas)
    # CLICK ANALYSIS
    if group == 1:
        clicks = clicks_per_song(data)
        cpcms = clicks_per_centms(clicks)
        tpc = time_per_clicks(clicks)
    else:
        cpcms = tpc = 0
    return segs_songs, nasa_result, cpcms, tpc


def compute_res(ref, data):
    seg_stats = compute_segs_accuracy(ref, data) #Does not work, to debug
    return seg_stats


def print_data(row_data, path, group, segs_songs, nasa_result, cpcms, tpc):
    # SEGMENTATION ANALYSIS

    # print_segs_results_subjects(segs_songs, path)
    '''print_segs_results(segs_songs, path)
    print_segs_results_max(segs_songs, 100, path)
    print_segs_results_max(segs_songs, 1000, path)'''

    # NASA ANALYSIS
    print_nasa_results(row_data, path+"nasatlx/overallpondere/", nasa_result[1])
    print_nasa_results(row_data, path+"nasatlx/exmentale/", nasa_result[2])
    print_nasa_results(row_data, path+"nasatlx/exphy/", nasa_result[3])
    print_nasa_results(row_data, path+"nasatlx/extemp/", nasa_result[4])
    print_nasa_results(row_data, path+"nasatlx/perf/", nasa_result[5])
    print_nasa_results(row_data, path+"nasatlx/effort/", nasa_result[6])
    print_nasa_results(row_data, path+"nasatlx/frustration/", nasa_result[7])
    print_nasa_results(row_data, path+"nasatlx/overallnonpondere/", nasa_result[8])


    # CLICK ANALYSIS
    if group == 1:
        '''print_click_results_nb(cpcms, path)
        print_click_results_nb_mean(cpcms, path)
        print_click_results_time(tpc, path)
        print_click_results_time_mean(tpc, path) # A verifier
        print_click_results_time_all(tpc, path)'''

def experiment(row_data, path_figs, path_data):
    group = path_data[-2]
    data = process_data(row_data, path_data)
    segs_songs, nasa_result, cpcms, tpc = compute_data(data, group)
    print_data(row_data, path_figs, group, segs_songs, nasa_result, cpcms, tpc)

def main():
    # GROUP 1: dual-task
    #all
    path_data = 'C:/Users/jmoca/OneDrive/Documents/Travail/These/Etude_Cognitive/exp1-cognitive-load/' \
                'resultats_exp1/csv_finaux/data1/resultats_exp1_1_'
    path_figs = "cognitive_algorithm_and_its_musical_applications/src/exp/cogload/figures/data_1/"
    '''path = path_figs + "all/"
    exp_1 = [34, 35, 36, 38, 39, 40, 63, 64, 65, 67, 68]
    experiment(exp_1, path, path_data)

    #level1
    path = path_figs + "niveau1/"
    exp_1 = [35, 68]
    experiment(exp_1, path, path_data)

    #level2
    path = path_figs + "niveau2/"
    exp_1 = [34, 36, 38, 39, 40, 63, 64, 65, 67]
    experiment(exp_1, path, path_data)

    #vents
    path = path_figs + "vent/"
    exp_1= [34, 39, 63, 65, 67]
    experiment(exp_1, path, path_data)

    #piano-cordes
    path = path_figs + "piano-cordes/"
    exp_1 = [34, 35, 36, 38, 40, 63, 64, 68]
    experiment(exp_1, path, path_data)

    #piano
    path = path_figs + "piano/"
    exp_1 = [34, 35, 36, 38, 63, 64]
    experiment(exp_1, path, path_data)

    #cordes
    path = path_figs + "cordes/"
    exp_1 = [34, 35, 36, 40, 63, 68]
    experiment(exp_1, path, path_data)'''

    path = path_figs + "ventinstru1/"
    exp_1= [39, 63, 65, 67]
    experiment(exp_1, path, path_data)

    path = path_figs + "ventunique/"
    exp_1= [39, 65, 67]
    experiment(exp_1, path, path_data)

    # GROUP 2: single-task
    #all
    '''path_data = 'C:/Users/jmoca/OneDrive/Documents/Travail/These/Etude_Cognitive/exp1-cognitive-load/' \
                'resultats_exp1/csv_finaux/data2/resultats_exp1_2_'
    path_figs = "cognitive_algorithm_and_its_musical_applications/src/exp/cogload/figures/data_2/"
    path = path_figs + "all/"
    exp_2 = [1, 3, 4, 7, 8, 11, 12, 14, 16, 17, 18]
    experiment(exp_2, path, path_data)

    #level0
    path = path_figs + "niveau0/"
    exp_2 = [1, 8, 11]
    experiment(exp_2, path, path_data)

    #level1
    path = path_figs + "niveau1/"
    exp_2 = [4, 7, 12, 14, 16, 18]
    experiment(exp_2, path, path_data)

    #level2
    path = path_figs + "niveau2/"
    exp_2 = [3, 17]
    experiment(exp_2, path, path_data)

    #batterie
    path = path_figs + "batterie/"
    exp_2 = [7, 11, 12, 18]
    experiment(exp_2, path, path_data)

    #guitare
    path = path_figs + "guitare/"
    exp_2 = [1, 4, 8, 11, 12, 14, 16, 17]
    experiment(exp_2, path, path_data)

    #piano, violon, compo
    path = path_figs + "piano-violon-compo/"
    exp_2 = [3, 4, 12, 17]
    experiment(exp_2, path, path_data)'''


main()