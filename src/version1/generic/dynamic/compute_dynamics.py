import parameters as prm
from matplotlib.pyplot import *
import data_computing as dc
import similarity_functions as sf

SHOW_FREQUENCIES = 0

NB_SILENCE = prm.NB_SILENCE
hop_length = prm.HOP_LENGTH
init = prm.INIT
nb_values = prm.NB_VALUES
fmin = prm.NOTE_MIN

PRINT_GRAPHES = 1


def graph_energy(tab, rate, data_size, name, y_label):
    figure(figsize=(100, 30))
    graph_title = "Graph of " + y_label + " : sequence " + name
    title(graph_title)
    nb_frame = len(tab)
    frames = np.arange(nb_frame)*data_size/(rate * nb_frame)*hop_length
    plot(frames, tab)
    xlabel("time (s)")
    ylabel(y_label)
    axis([0, data_size/rate*hop_length, min(tab) - abs(min(tab)/10), max(tab) + max(tab)/10])
    figname = "cognitive_algorithm_and_its_musical_applications/src/generic/dynamic/" + name + "_" + y_label + ".png"
    print(figname)
    savefig(figname)
    show()


def compute_dynamics():
    audio_path = prm.PATH_SOUND + prm.NAME + prm.FORMAT
    name = audio_path.split('/')[-1].split('.')[0]
    data, rate, data_size, data_duration_in_s = dc.get_data(audio_path)

    nb_points = NB_SILENCE
    a = np.zeros(nb_points)
    data = np.concatenate((a, data))
    nb_sil_frames = nb_points / hop_length
    nb_hop = int(data_size / hop_length + nb_sil_frames) + 1
    if data_size % hop_length < init:
        nb_hop = int(data_size / hop_length)

    v_tab, s_tab = dc.get_descriptors(data, rate, hop_length, nb_hop, nb_values, init, fmin)
    print("len stab",len(s_tab[0]))
    print(nb_hop)

    if prm.FFT_BIT == 1:
        s_tab_trans = np.array(s_tab).transpose()
    else:
        s_tab_trans = s_tab.transpose()

    vsd = [0]
    vsd_temp = [0]
    vdd = [0]
    vdd_temp = [0]
    vkl = [0]
    vkl_temp = [0]
    fsd = [0]
    fsd_temp = [0]
    fdd = [0]
    fdd_temp = [0]
    for i in range(1, len(v_tab)):
        vsd_temp.append(1 - sf.volume_static_similarity(v_tab, i, i - 1))
        vdd_temp.append(sf.volume_dynamic_dissimilarities(v_tab, i, i - 1))
        vkl_temp.append(sf.volume_kullback_leibler(v_tab, i, i - 1))
        fsd_temp.append(1 - sf.frequency_static_similarity_cqt(s_tab_trans, i, i - 1))
        fdd_temp.append(sf.frequency_dynamic_dissimilarity_mfcc_cqt(s_tab, i, i - 1))

    for i in range(1, len(v_tab)):
        vsd.append(vsd_temp[i]/max(vsd_temp))
        vdd.append(vdd_temp[i]/max(vdd_temp))
        vkl.append(vkl_temp[i]/max(vkl_temp))
        fsd.append(fsd_temp[i]/max(fsd_temp))
        fdd.append(fdd_temp[i]/max(fdd_temp))

    if PRINT_GRAPHES == 1:
        graph_energy(v_tab, rate, nb_hop, name, "volume")
        print(v_tab)
        graph_energy(vsd, rate, nb_hop, name, "volume static dissimilarity")
        print(vsd)
        graph_energy(vdd, rate, nb_hop, name, "volume dynamic dissimilarity")
        print(vdd)
        graph_energy(vkl, rate, nb_hop, name, "volume kullback leibler dissimilarity")
        print(vkl)
        graph_energy(fsd, rate, nb_hop, name, "frequency static dissimilarity")  # concordance différentielle
        print(fsd)
        graph_energy(fdd, rate, nb_hop, name, "frequency dynamic dissimilarity")
        print(fdd)

    return vsd, vdd, vkl, fsd, fdd


#compute_dynamics()
