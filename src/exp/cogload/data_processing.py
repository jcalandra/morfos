import numpy as np
import csv

blue_value = 0

def process_data(exp_1, path_data):
    data_1 = []
    for ind in exp_1:
        path = path_data + str(ind) + '.csv'
        with open(path, newline='') as csvfile:
            popreader = csv.reader(csvfile, delimiter=',', quotechar='"')
            datalist = list(popreader)

        i = 0
        while i < len(datalist):
            j = 1
            n = len(datalist[i])
            while j < n and (datalist[i][n - j] == '' or datalist[i][n - j] == ' '):
                datalist[i].pop(n - j)
                j += 1
            if j == n and datalist[i][0] == '':
                # datalist.pop(i)
                datalist[i][0] = '0'
                #datalist[i].append('1')
            else:
                i += 1

        segment_prelist = datalist[0:43]
        question_prelist = datalist[43:52]
        nasatlx_prelist = datalist[52:170]
        clicks_prelist = datalist[170:]

        segment_list = []
        question_list = question_prelist[1:]
        nasatlx_list = []
        clicks_list = []
        for i in range(1, len(segment_prelist)):
            if i % 3 != 1:
                seg = []
                for j in segment_prelist[i]:
                    seg.append(int(j))
                segment_list.append(seg)
        for i in range(1, len(nasatlx_prelist)):
            if i % 9 != 1:
                nasatlx_list.append(nasatlx_prelist[i])
        for i in range(1, len(clicks_prelist)):
            if i % 3 != 1:
                click = []
                for j in clicks_prelist[i]:
                    if j == '' or j == 'b':
                        click.append(blue_value)
                    else:
                        click.append(int(j))
                clicks_list.append(click)
        data_1x = [segment_list, question_list, nasatlx_list, clicks_list]
        data_1.append(data_1x)

    return data_1


def preprocess_segs():
    path = 'C:/Users/jmoca/OneDrive/Documents/Travail/These/Etude_Cognitive/exp1-cognitive-load/' \
           'resultats_exp1/csv_finaux/segmentations_1.csv'
    with open(path, newline='') as csvfile:
        popreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        segslist = list(popreader)

    # removing blank cells
    ind = 0
    while ind < len(segslist):
        j = 1
        n = len(segslist[ind])
        while j < n and (segslist[ind][n - j] == '' or segslist[ind][n - j] == ' '):
            segslist[ind].pop(n - j)
            j += 1
        if j == n and segslist[ind][n - j] == '':
            segslist.pop(ind)
        else:
            ind += 1
    # reformating lines
    segs_tab = []
    new_tab = []
    for i in segslist:
        if len(i) == 1:
            if len(new_tab) > 0:
                segs_tab.append(new_tab)
            new_tab = []
        else:
            new_tab.append(i)
    segs_tab.append(new_tab)
    return segs_tab


def convert_segs(segs_tab):
    segs_tab_ms = []
    for song in segs_tab:
        new_song = []
        for seg in song:
            new_seg = []
            for time in seg[:-1]:
                if time == '0':
                    minute = '00'
                    sec = '00'
                    milisec = '000'
                else:
                    minute = time[0:2]
                    sec = time[3:5]
                    milisec = time[6:]

                new_time = int(minute)*60*1000 + int(sec)*1000 + int(milisec)
                new_seg.append(new_time)
            new_song.append(new_seg)
        segs_tab_ms.append(new_song)
    return segs_tab_ms


def process_segs():
    presegs = preprocess_segs()
    segs = convert_segs(presegs)
    return segs


def list2intervals(inilist):
    n = len(inilist)
    intervals = np.zeros((n - 1, 2))
    for i in range(n - 1):
        intervals[i, 0] = inilist[i]
        intervals[i, 1] = inilist[i + 1]
    return intervals