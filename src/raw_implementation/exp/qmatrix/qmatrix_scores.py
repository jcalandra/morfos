from rwcpop_parser import rwcpop_csv2list
from qmatrix_exp1 import qmat_protocol1
from qmatrix_exp2 import qmat_protocol2
from numpy import load, zeros
from raw_implementation import parameters, main_mso_char, main_mso
import mir_eval
import csv
import os
import shutil
import time

# import qmatrix_params

TO_WRITE = 1
nb_exp = 3
# nb_run = qmatrix_params.nb_run


def qmatrix_compute_fd(song, result_path):
    if song < 10:
        number = '0' + str(song)
    else:
        number = str(song)
    path = "/data/qmatrix/"
    if nb_exp == 1:
        q_matrix = load(f"{path}/Qmatrix_song{song}.npy", allow_pickle=True)
        qmat_symbols, qmatrix_inter2, qmatrix_inter = qmat_protocol1(q_matrix)
        main_mso_char.main(qmat_symbols, result_path)
    elif nb_exp == 2:
        q_matrix = load(f"{path}/Qmatrix_song{song}.npy", allow_pickle=True)
        qmat_symbols, qmatrix_inter2, qmatrix_inter, qmatrix_diff = qmat_protocol2(q_matrix)
        main_mso_char.main(qmat_symbols, result_path)
    elif nb_exp == 3:
        path += "/Qmatrix_song"+ str(song) + ".npy"
        result_path = parameters.project_root + '/results/qmatrix/exp3/qmatrix/Pop ' + number + '/'
        main_mso.main(path, result_path)


def qmatrix_list2section(poplist):
    section = []
    section_timer = zeros((len(poplist), 2))
    ext_char = ['(',')','/','|', '*', '~', "'", '#', '-']
    new_timer = 0
    for i in range(10):
        ext_char.append(str(i))
    for row_id in range(len(poplist)):
        while poplist[row_id][-1] == '':
            poplist[row_id] = poplist[row_id][:-1]
        section_char_id = 0
        if len(poplist[row_id][0]) > 1:
            while poplist[row_id][0][section_char_id] in ext_char:
                section_char_id += 1
        section.append([poplist[row_id][0][section_char_id]])
        last_timer = new_timer
        new_timer = last_timer + len(poplist[row_id]) - 2
        if poplist[row_id][-1][0] == "[":
            new_timer -= 1
        section_timer[row_id, 0] = last_timer
        section_timer[row_id, 1] = new_timer
    return section, section_timer


def qmatrix_parse_ref_sec(path):
    poplist = rwcpop_csv2list(path)
    ref_label, ref_interval = qmatrix_list2section(poplist)
    return ref_label, ref_interval



def qmatrix_parse_est(test_path, result_path, ref_intervals):
    qmatrix_compute_fd(test_path, result_path)
    objs = main_mso_char.obj_s.objects
    est_labels_all = []
    est_intervals_all = []
    time_max = ref_intervals[-1, 1]
    for level in range(len(objs)):
        est_labels_all.append([])
        est_intervals_all.append(zeros((len(objs[level]), 2)))
        for j in range(len(objs[level])):
            est_labels_all[level].append(str(objs[level][j]["coordinates"]["y"]))
            if j == 0:
                last_timer = 0
            else:
                last_timer = objs[level][j - 1]["coordinates"]["x"]
            if last_timer < time_max:
                est_intervals_all[level][j, 0] = last_timer
                est_intervals_all[level][j, 1] = objs[level][j]["coordinates"]["x"]
            else:
                est_intervals_all[level] = est_intervals_all[level][:j]
                est_labels_all[level] = est_labels_all[level][:j]
                break
    return est_labels_all, est_intervals_all


def rwcpop_compute_scores(nb_run):
    min_val = 1
    max_val = 100
    nb_samples = max_val - min_val # +1 if pop53 were counted
    means = {'Precision@0.5': 0, 'Recall@0.5': 0, 'F-measure@0.5': 0,
             'Precision@3.0': 0, 'Recall@3.0': 0, 'F-measure@3.0': 0,
             'Ref-to-est deviation': 0, 'Est-to-ref deviation': 0,
             'Pairwise Precision': 0, 'Pairwise Recall': 0, 'Pairwise F-measure': 0,
             'Rand Index': 0, 'Adjusted Rand Index': 0,
             'Mutual Information': 0, 'Adjusted Mutual Information': 0, 'Normalized Mutual Information': 0,
             'NCE Over': 0, 'NCE Under': 0, 'NCE F-measure': 0,
             'V Precision': 0, 'V Recall': 0, 'V-measure': 0}
    if TO_WRITE:
        os.mkdir(parameters.project_root + '/results/qmatrix/run' + str(nb_run))
        os.mkdir(parameters.project_root + '/results/qmatrix/run' + str(nb_run) + '/exp' + str(nb_exp))
        os.mkdir(parameters.project_root + '/results/qmatrix/run' + str(nb_run) + '/exp' + str(nb_exp) + '/qmatrix/')
        csvfile_all_all = open(parameters.project_root + '/results/qmatrix/all_scores.csv', 'a', newline='')
        csvwriter_all_all = csv.writer(csvfile_all_all, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        file_all_scores = open(parameters.project_root + '/results/qmatrix/run' + str(nb_run) + '/exp' + str(nb_exp) + '/scores_goodlevel.txt', "a")
        csvfile_all_scores = open(parameters.project_root + '/results/qmatrix/run' + str(nb_run) + '/exp' + str(nb_exp) + '/scores_goodlevel.csv', 'w', newline='')
        csvwriter_all_scores = csv.writer(csvfile_all_scores, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in range(min_val,max_val + 1):
        if i < 10:
            number = '0' + str(i)
        else:
            number = str(i)
        if i == 53:
            continue
        print("ANALYSIS NUMBER " + str(number))
        test_path = parameters.project_root + '/data/rwcpop/Pop ' + number + ' (grid).csv'
        result_path = parameters.project_root + '/results/qmatrix/run' + str(nb_run) + '/exp' + str(nb_exp) + '/qmatrix/Pop ' + number + '/'

        ref_labels, ref_intervals = qmatrix_parse_ref_sec(test_path)
        est_labels_all, est_intervals_all = qmatrix_parse_est(i, result_path, ref_intervals)


        if TO_WRITE:
            file_scores = open(result_path[:-7] + "scores"+number+".txt", "w")
            csvfile_scores = open(result_path[:-7] + "scores"+number+".csv", 'w', newline='')
            csvwriter_scores = csv.writer(csvfile_scores, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        best_scores = 0
        best_scores_line = "no best score"
        best_level = 0

        for level in range(0,len(est_labels_all)):
            est_labels = est_labels_all[level]
            est_intervals = est_intervals_all[level]
            scores = mir_eval.segment.evaluate(ref_intervals, ref_labels, est_intervals, est_labels)
            # 'Pairwise F-measure' or
            # 'F-measure@0.5' or
            # 'Recall@0.5'
            if scores['F-measure@0.5'] > best_scores:
                best_scores = scores['F-measure@0.5']
                best_scores_line = scores
                best_level = level

            if TO_WRITE:
                file_scores.write("Scores at level" + str(level) + "\n")
                file_scores.write(str(scores) + "\n")
                if level == 0:
                    csvwriter_scores.writerow(['file number'] + ['level'] + [i for i,j in scores.items()])
                csvwriter_scores.writerow([number] + [level] + [round(j, 2) for i,j in scores.items()])

        for key, value in means.items():
            means[key] = means[key] + best_scores_line[key]

        if TO_WRITE:
            file_scores.close()
            csvfile_scores.close()
            if i == min_val:
                csvwriter_all_scores.writerow(['file number'] + ['level'] + [i for i,j in best_scores_line.items()])
            file_scores.close()
            file_all_scores.write("best scores for file n°" + str(number) + "at level " + str(best_level) +"\n")
            file_all_scores.write(str(best_scores_line) + "\n")
            csvwriter_all_scores.writerow([number] + [level] + [round(j, 2) for i,j in best_scores_line.items()])

    for key, value in means.items():
        means[key] = means[key]/nb_samples

    if TO_WRITE:
        file_all_scores.write("mean scores :" + "\n")
        file_all_scores.write(str(means) + "\n")
        csvwriter_all_scores.writerow(["mean"] + ["none"] + [round(j, 2) for i,j in means.items()])
        csvwriter_all_all.writerow(["mean " + str(nb_run)] + ["none"] + [round(j, 2) for i,j in means.items()])
        file_all_scores.close()
        csvfile_all_scores.close()
        csvfile_all_all.close()
        shutil.copyfile(parameters.project_root + '/src/data.json', result_path[:-7] + 'parameters.json')
        time.sleep(30)


#rwcpop_compute_scores(nb_run)