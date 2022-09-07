from data_processing import process_segs, process_data
from structure_measures import compute_segs_accuracy, segs_per_song
from cogload_measures import clicks_per_song, mean_click_sujet, mean_click

def main():
    exp_1 = [1, 8, 10, 12, 19, 20, 22, 23, 24, 26, 27, 28]
    exp_1 = [1, 8, 10, 12]
    segs = process_segs()
    data_1 = process_data(exp_1)
    seg_stats = compute_segs_accuracy(segs, data_1)
    segs_per_song(data_1)
    clicks_per_song(data_1)
    mc = mean_click_sujet(data_1)
    mean_click(mc)


main()