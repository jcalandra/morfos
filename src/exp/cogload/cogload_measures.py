from data_processing import blue_value
import matplotlib.pyplot as plt
import numpy as np

TO_SAVE = 1
figure_size = (21,14)

#CLICKS
def clicks_per_song(data):
    clicks = [[] for i in range(len(data[0][3])//2)]
    for sujet in data:
        for c in range(len(sujet[3])):
            if c%2 == 0:
                couple = [sujet[3][c], sujet[3][c + 1]]
                clicks[c//2].append(couple)
    return clicks


def time_per_clicks(cps):
    tpc = cps.copy()
    for song in range(len(tpc)):
        for subject in range(len(tpc[song])):
            if tpc[song][subject][0][0] != 0:
                tpc[song][subject][0][0] = cps[song][subject][1][0]/abs(cps[song][subject][0][0])
                tpc[song][subject][1][0] = cps[song][subject][1][0]
                for i in range(1, len(tpc[song][subject][0])):
                    tpc[song][subject][0][i] = cps[song][subject][1][i]/abs(cps[song][subject][0][i])
                    tpc[song][subject][1][i] = tpc[song][subject][1][i - 1] + cps[song][subject][1][i]
    return tpc


def clicks_per_centms(cps):
    cpcms = []
    for song in range(len(cps)):
        song_tab = []
        for subject in range(len(cps[song])):
            subject_tab = []
            subject_tab_click = []
            subject_tab_time = []
            t_tot = 0
            for i in range(len(cps[song][subject][0])):
                if cps[song][subject][0][0] != 0:
                    yi = cps[song][subject][0][i]*100/(cps[song][subject][1][i])
                else:
                    yi = 0
                t_tot_new = t_tot + cps[song][subject][1][i]
                for j in range(int(t_tot_new) - int(t_tot)):
                    subject_tab_click.append(yi)
                    subject_tab_time.append(len(subject_tab_time)*100)
                t_tot = t_tot_new
            subject_tab.append(subject_tab_click)
            subject_tab.append(subject_tab_time)
            song_tab.append(subject_tab)
        cpcms.append(song_tab)
    return cpcms


def mean_click_sujet(data):
    mean_click = []
    for sujet in data:
        sujet_click = []
        for c in range(len(sujet[3])):
            if c%2 == 0:
                sum_n = 0
                sum_t = 0
                for i in range(len(sujet[3][c])):
                    if sujet[3][c][i] != blue_value:
                        sum_n += sujet[3][c][i]
                        sum_t += sujet[3][c + 1][i]
                sujet_click.append(sum_t/sum_n)
        mean_click.append(sujet_click)
    return mean_click


def print_click_results_time(tpc, path_figs):
    for songs in range(len(tpc)):
        fig, ax = plt.subplots(len(tpc[songs]),1, figsize=figure_size, sharex='all', sharey='all')
        fig.suptitle("mean click duration in function of time of song n°" + str(songs))
        plt.xlabel("temps (ms)")
        plt.ylabel("mean click duration (ms)")
        subject = 0
        for axi in ax:
            axi.plot(tpc[songs][subject][1], tpc[songs][subject][0], linewidth=0.8, markersize=2,
                     label="subject n° " + str(subject))
            subject += 1
        if TO_SAVE:
            name = path_figs + "clicks/results_time_" + str(songs) \
               + ".png"
            plt.savefig(name)
    if not TO_SAVE:
        plt.show()


def print_click_results_nb(cpcms, path_figs):
    for songs in range(len(cpcms)):
        fig, ax = plt.subplots(len(cpcms[songs]),1, figsize=figure_size,sharex='all', sharey='all')
        fig.suptitle("mean number of click per 100ms in function of time of song n°" + str(songs))
        plt.xlabel("temps (ms)")
        plt.ylabel("mean number of click per 100ms")
        subject = 0
        for axi in ax:
            axi.plot(cpcms[songs][subject][1], cpcms[songs][subject][0], linewidth=0.8, markersize=2,
                     label="subject n° " + str(subject))
            subject += 1
        if TO_SAVE:
            name = path_figs +"clicks/results_nb_" + str(songs) \
                   + ".png"
            plt.savefig(name)
    if not TO_SAVE:
        plt.show()


def print_click_results_time_all(tpc, path_figs):

    for songs in range(len(tpc)):
        plt.figure(figsize=figure_size)
        plt.title("mean click duration in function of time of song n°" + str(songs))
        plt.xlabel("temps")
        plt.ylabel("mean click duration")
        for subject in range(len(tpc[songs])):
            plt.plot(tpc[songs][subject][1], tpc[songs][subject][0], linewidth=0.8, markersize=2,
                     label="subject n° " + str(subject))

        if TO_SAVE:
            name = path_figs + "clicks/results_time_all" + str(songs) \
                   + ".png"
            plt.savefig(name)
    if not TO_SAVE:
        plt.show()


def print_click_results_nb_mean(cpcms, path_figs):
    for songs in range(len(cpcms)):
        plt.figure(figsize=figure_size)

        plt.title("mean number of click per 100ms in function of time of song n°" + str(songs))
        plt.xlabel("temps (ms)")
        plt.ylabel("mean number of click per 100ms")
        max_len_song = 0
        for subject in range(len(cpcms[songs])):
            if len(cpcms[songs][subject][0]) > max_len_song:
                max_len_song = len(cpcms[songs][subject][0])

        mean_songs = [0 for i in range(max_len_song)]
        for subject in range(len(cpcms[songs])):
            for i in range(min(len(mean_songs),len(cpcms[songs][subject][0]))):
                mean_songs[i] += cpcms[songs][subject][0][i]
        for i in range(len(mean_songs)):
            mean_songs[i] /= len(cpcms[songs])

        plt.plot([i*100 for i in range(max_len_song)], mean_songs, linewidth=0.8, markersize=2,
                     label="subject n° " + str(subject))

        if TO_SAVE:
            name = path_figs + "clicks/results_nb_mean" + str(songs) \
                   + ".png"
            plt.savefig(name)

    if not TO_SAVE:
        plt.show()


def print_click_results_time_mean(cpcms, path_figs): #todo: change by tpc
    for songs in range(len(cpcms)):
        plt.figure(figsize=figure_size)

        plt.title("click duration in function of time of song n°" + str(songs))
        plt.xlabel("temps (ms)")
        plt.ylabel("click duration")
        max_len_song = 0
        for subject in range(len(cpcms[songs])):
            if len(cpcms[songs][subject][0]) > max_len_song:
                max_len_song = len(cpcms[songs][subject][0])

        mean_songs = [0 for i in range(max_len_song)]
        for subject in range(len(cpcms[songs])):
            for i in range(min(len(mean_songs),len(cpcms[songs][subject][0]))):
                mean_songs[i] += cpcms[songs][subject][0][i]
        for i in range(len(mean_songs)):
            mean_songs[i] /= len(cpcms[songs])

        plt.plot([i*100 for i in range(max_len_song)], mean_songs, linewidth=0.8, markersize=2,
                 label="subject n° " + str(subject))

        if TO_SAVE:
            name = path_figs + "clicks/results_time_mean" + str(songs) \
                   + ".png"
            plt.savefig(name)

    if not TO_SAVE:
        plt.show()


# SEGMENTATION
def segs_per_song(data):
    segs = [[] for i in range(len(data[0][0])//2)]
    for sujet in data:
        for c in range(len(sujet[0])):
            if c%2 == 0:
                couple = [sujet[0][c], sujet[0][c + 1]]
                segs[c//2].append(couple)
    return segs


def print_segs_results_subjects(segs, path_figs):

    for songs in range(len(segs)):
        fig, ax = plt.subplots(len(segs[songs]),1, figsize=figure_size, sharex='all', sharey='all')
        fig.suptitle("segmentation of song n°" + str(songs))
        plt.xlabel("temps")
        plt.ylabel("onset")
        subject = 0
        for axi in ax:
            onsets_phrase = [1 for i in range(len(segs[songs][subject][0]))]
            onsets_section = [2 for i in range(len(segs[songs][subject][1]))]

            axi.plot(segs[songs][subject][0], onsets_phrase, ":o", linewidth=0.8, markersize=2,
                     label="subject n° " + str(subject))
            axi.plot(segs[songs][subject][1], onsets_section,":o", linewidth=0.8, markersize=2,
                     label="subject n° " + str(subject))
            subject += 1
        if TO_SAVE:
            name = path_figs + "segs/results_subjects" + str(songs) \
                   + ".png"
            plt.savefig(name)

    if not TO_SAVE:
        plt.show()


def print_segs_results(segs, path_figs):

    for songs in range(len(segs)):
        plt.figure(figsize=figure_size)
        plt.title("segmentation of song n°" + str(songs))
        plt.xlabel("temps")
        plt.ylabel("onset")
        for subject in range(len(segs[songs])):
                onsets_phrase = [subject for i in range(len(segs[songs][subject][0]))]
                onsets_section = [20+subject for i in range(len(segs[songs][subject][1]))]

                plt.plot(segs[songs][subject][0], onsets_phrase, ":o", linewidth=0.8, markersize=2,
                     label="subject n° " + str(subject))
                plt.plot(segs[songs][subject][1], onsets_section,":o", linewidth=0.8, markersize=2,
                         label="subject n° " + str(subject))

        if TO_SAVE:
            name = path_figs + "segs/results" + str(songs) \
                   + ".png"
            plt.savefig(name)
    if not TO_SAVE:
        plt.show()

def print_segs_results_max(segs, div, path_figs):

    for songs in range(len(segs)):
        max_length_phrase = 0
        max_length_section = 0
        for subject in range(len(segs[songs])):
            if segs[songs][subject][0][-1] > max_length_phrase:
                max_length_phrase = segs[songs][subject][0][-1]
            if segs[songs][subject][1][-1] > max_length_section:
                max_length_section = segs[songs][subject][1][-1]

        sum_phrase = [0 for i in range(int(max_length_phrase/div))]
        sum_section = [0 for i in range(int(max_length_section/div))]

        for subject in range(len(segs[songs])):
            for i in range(len(sum_phrase)):
                for j in range(len(segs[songs][subject][0])):
                    if i == int(segs[songs][subject][0][j]/div):
                        sum_phrase[i] += 1

            for i in range(len(sum_section)):
                for j in range(len(segs[songs][subject][1])):
                    if i == int(segs[songs][subject][1][j]/div):
                        sum_section[i] += 1

        plt.figure(figsize=figure_size)
        plt.title("segmentation of song n°" + str(songs))
        plt.xlabel("temps")
        plt.ylabel("onset")
        plt.plot([i for i in range(len(sum_phrase))], sum_phrase, ":o", linewidth=0.8, markersize=2, label="subject n° " + str(subject))
        plt.plot([i for i in range(len(sum_section))], sum_section,":o", linewidth=0.8, markersize=2, label="subject n° " + str(subject))
        if TO_SAVE:
            name = path_figs + "segs/results_max" + str(songs) + "_" +str(div) \
                   + ".png"
            plt.savefig(name)
    if not TO_SAVE:
        plt.show()


def print_segs_clicks(segs, path_figs):

    for songs in range(len(segs)):
        fig, ax = plt.subplots(len(segs[songs]),1, figsize=figure_size, sharex='all', sharey='all')
        fig.suptitle("segmentation of song n°" + str(songs))
        plt.xlabel("temps")
        plt.ylabel("onset")
        subject = 0
        for axi in ax:
            onsets_phrase = [1 for i in range(len(segs[songs][subject][0]))]
            onsets_section = [2 for i in range(len(segs[songs][subject][1]))]

            axi.plot(segs[songs][subject][0], onsets_phrase, ":o", linewidth=0.8, markersize=2,
                     label="subject n° " + str(subject))
            axi.plot(segs[songs][subject][1], onsets_section,":o", linewidth=0.8, markersize=2,
                     label="subject n° " + str(subject))
            subject += 1
        if TO_SAVE:
            name = path_figs + "segs/results_subjects" + str(songs) \
                   + ".png"
            plt.savefig(name)

    if not TO_SAVE:
        plt.show()


# NASATLX
def nasatlx_per_subject(data):
    nasas = [[] for i in range(len(data))]
    i = 0
    for sujet in data:
        nasas[i] = sujet[2]
        i += 1
    return nasas


def nasaresult_overall_per_subject(nasas):
    nasa_results = [[] for i in range(len(nasas))]
    for subject in range(len(nasas)):
        nasa_ri = []
        for value in range(len(nasas[subject])):
            if value%8 == 7:
                if len(nasas[subject][value]) == 1:
                    nasa_ri.append(None)
                else:
                    nasa_ri.append(round(float(nasas[subject][value][1]),2))
        nasa_results[subject] = nasa_ri

    return nasa_results


def nasaresult_per_subject(nasas):
    # RESULT KNOW
    all_nasa_results = []
    nasa_results = [[] for i in range(len(nasas))]
    for subject in range(len(nasas)):
        nasa_ri = []
        for value in range(len(nasas[subject])):
            if value%8 == 0:
                if len(nasas[subject][value]) == 1:
                    nasa_ri.append(None)
                else:
                    nasa_ri.append(int(nasas[subject][value][1]))
        nasa_results[subject] = nasa_ri
    print(nasa_results)
    all_nasa_results.append(nasa_results)

    #OVERALL PONDERE
    nasa_results = [[] for i in range(len(nasas))]
    for subject in range(len(nasas)):
        nasa_ri = []
        for value in range(len(nasas[subject])):
            if value%8 == 7:
                if len(nasas[subject][value]) == 1:
                    nasa_ri.append(None)
                else:
                    nasa_ri.append(round(float(nasas[subject][value][1]),2))
        nasa_results[subject] = nasa_ri
    all_nasa_results.append(nasa_results)

    #EXIGENCE MENTALE
    nasa_results = [[] for i in range(len(nasas))]
    for subject in range(len(nasas)):
        nasa_ri = []
        for value in range(len(nasas[subject])):
            if value%8 == 1:
                if len(nasas[subject][value]) == 1:
                    nasa_ri.append(None)
                else:
                    nasa_ri.append(round(float(nasas[subject][value][3]),2))
        nasa_results[subject] = nasa_ri
    all_nasa_results.append(nasa_results)

    #EXIGENCE PHYSIQUE
    nasa_results = [[] for i in range(len(nasas))]
    for subject in range(len(nasas)):
        nasa_ri = []
        for value in range(len(nasas[subject])):
            if value%8 == 2:
                if len(nasas[subject][value]) == 1:
                    nasa_ri.append(None)
                else:
                    nasa_ri.append(round(float(nasas[subject][value][3]),2))
        nasa_results[subject] = nasa_ri
    all_nasa_results.append(nasa_results)

    #EXIGENCE TEMPORELLE
    nasa_results = [[] for i in range(len(nasas))]
    for subject in range(len(nasas)):
        nasa_ri = []
        for value in range(len(nasas[subject])):
            if value%8 == 3:
                if len(nasas[subject][value]) == 1:
                    nasa_ri.append(None)
                else:
                    nasa_ri.append(round(float(nasas[subject][value][3]),2))
        nasa_results[subject] = nasa_ri
    all_nasa_results.append(nasa_results)

    #PERFORMANCE
    nasa_results = [[] for i in range(len(nasas))]
    for subject in range(len(nasas)):
        nasa_ri = []
        for value in range(len(nasas[subject])):
            if value%8 == 4:
                if len(nasas[subject][value]) == 1:
                    nasa_ri.append(None)
                else:
                    nasa_ri.append(round(float(nasas[subject][value][3]),2))
        nasa_results[subject] = nasa_ri
    all_nasa_results.append(nasa_results)

    #EFFORT
    nasa_results = [[] for i in range(len(nasas))]
    for subject in range(len(nasas)):
        nasa_ri = []
        for value in range(len(nasas[subject])):
            if value%8 == 5:
                if len(nasas[subject][value]) == 1:
                    nasa_ri.append(None)
                else:
                    nasa_ri.append(round(float(nasas[subject][value][3]),2))
        nasa_results[subject] = nasa_ri
    all_nasa_results.append(nasa_results)

    #FRUSTRATION
    nasa_results = [[] for i in range(len(nasas))]
    for subject in range(len(nasas)):
        nasa_ri = []
        for value in range(len(nasas[subject])):
            if value%8 == 6:
                if len(nasas[subject][value]) == 1:
                    nasa_ri.append(None)
                else:
                    nasa_ri.append(round(float(nasas[subject][value][3]),2))
        nasa_results[subject] = nasa_ri
    all_nasa_results.append(nasa_results)

    #OVERALL NON PONDERE
    nasa_results = [[] for i in range(len(nasas))]
    for subject in range(len(all_nasa_results[1])):
        nasa_ri = []
        for value in range(len(all_nasa_results[1][subject])):
            sum = 0
            if all_nasa_results[1][subject][value] == None:
                nasa_ri.append(None)
            else:
                for i in range(2,8):
                    sum += all_nasa_results[i][subject][value]/6
                nasa_ri.append(round(float(sum),2))
        nasa_results[subject] = nasa_ri
    all_nasa_results.append(nasa_results)

    return all_nasa_results


def mean_nasatlx(data):
    means = [0 for i in range(len(data[0][2])//8)]
    mean_len = [0 for i in range(len(data[0][2])//8)]
    for i in range(len(data)):
        for k in range(len(means)):
            if (data[i][2][k * 8 + 7][1]) != 'x' and data[i][2][k * 8][1] != 1:
                means[k] += float(data[i][2][k * 8 + 7][1])
                mean_len[k] += 1
    for k in range(len(means)):
        means[k] = means[k]/mean_len[k]
    return means



def print_nasa_results(raw_data, path_figs, nasa_results):
    # print NASA400 for every users
    x = np.arange(0, len(nasa_results), 1)
    Nasa400 = []
    for i in range(len(nasa_results)):
        if nasa_results[i][0] == None:
            Nasa400.append(0)
        else:
            Nasa400.append(int(nasa_results[i][0]*10)/10)
    plt.figure(figsize=figure_size)
    plt.title("NASA TLX results for 4 minutes of XO reproduction in silence")
    plt.xlabel("subject")
    plt.ylabel("overall result")
    plt.plot(x, Nasa400, ":o", linewidth=0, markersize=2)
    if TO_SAVE:
        name = path_figs + "results_nb_mean" + str(400) \
               + ".png"
        plt.savefig(name)

    # print NASA10,NASA11,NASA12 for every users
    plt.figure(figsize=figure_size)
    plt.title("NASATLX results of songs 10,11 and 12 for each participant")
    plt.xlabel("music label (increase by supposed difficulty)")
    plt.ylabel("overall result")
    mean_nasa = [0, 0, 0]
    nb_nasa = [0, 0, 0]
    for subject in range(len(nasa_results)):
        plt.plot([10, 11, 12], nasa_results[subject][1:4], ":o", linewidth=0.8, markersize=2,
                 label="subject n° " + str(raw_data[subject]))

        for j in range(len(mean_nasa)):
            if nasa_results[subject][j+1] != None:
                mean_nasa[j] += nasa_results[subject][j+1]
                nb_nasa[j] += 1
    for j in range(len(mean_nasa)):
        mean_nasa[j] = mean_nasa[j]/nb_nasa[j]
    plt.plot([10, 11, 12], mean_nasa, "-o", linewidth=1, markersize=2, color='black',
             label="mean by song")
    plt.legend()
    if TO_SAVE:
        name = path_figs + "10-12" \
               + ".png"
        plt.savefig(name)

    # print NASA1-9 for every users
    plt.figure(figsize=figure_size)
    plt.title("NASATLX results of songs 1 to 9 for each participant")
    plt.xlabel("music label (increase by supposed difficulty)")
    plt.ylabel("overall result")
    mean_nasa = [0 for i in range(0,9)]
    nb_nasa = [0 for i in range(0,9)]
    mean = [0, 0, 0]
    for subject in range(len(nasa_results)):
        plt.plot(np.arange(1, 10, 1), nasa_results[subject][4:], ":o", linewidth=0.8, markersize=2,
                 label="subject n° " + str(raw_data[subject]))

        for j in range(len(mean_nasa)):
            if nasa_results[subject][j+4] != None:
                mean_nasa[j] += nasa_results[subject][j+4]
                nb_nasa[j] += 1
    for j in range(len(mean_nasa)):
        mean_nasa[j] = mean_nasa[j]/nb_nasa[j]
        if j < 3:
            mean[0] += mean_nasa[j]
        if j >= 3 and j < 6 :
            mean[1] += mean_nasa[j]
        if j >= 6:
            mean[2] += mean_nasa[j]
    for i in range(len(mean)):
        mean[i] = mean[i]/3

    plt.plot(np.arange(1, 10, 1), mean_nasa, "-o", linewidth=1, markersize=2, color='black',
             label="mean by song")
    plt.plot(np.arange(1, 10, 3), mean, "-o", linewidth=1, markersize=2, color='red',
             label="mean by complexity level")
    plt.legend()
    if TO_SAVE:
        name = path_figs + "1-9"  \
               + ".png"
        plt.savefig(name)
    if not TO_SAVE:
        plt.show()
    return 0