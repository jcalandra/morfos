import rwcpop_parser_ref as rwcpp_ref
import rwcpop_parser_est as rwcpp_est
import module_parameters.parameters as prm
import mir_eval
import csv
import os


TO_WRITE = 1
test_path = rwcpp_est.project_root + '/../../data/rwcpop'
result_path = rwcpp_est.project_root + '/../../results/exp_rwcpop/version2/fmes3_60bpm/test1'

def rwcpop_compute_scores():
    min_val = 1
    max_val = 100
    tab_error = [6, 34, 36, 53, 94]
    # 6, 34 36, 53: all interval durations must be strictly positive
    # 18, 49, 66, 68, 69, 72 : alignment computation error
    nb_samples = max_val - min_val - len(tab_error) + 1
    means = {'Precision@0.5': 0, 'Recall@0.5': 0, 'F-measure@0.5': 0,
             'Precision@3.0': 0, 'Recall@3.0': 0, 'F-measure@3.0': 0,
             'Ref-to-est deviation': 0, 'Est-to-ref deviation': 0,
             'Pairwise Precision': 0, 'Pairwise Recall': 0, 'Pairwise F-measure': 0,
             'Rand Index': 0, 'Adjusted Rand Index': 0,
             'Mutual Information': 0, 'Adjusted Mutual Information': 0, 'Normalized Mutual Information': 0,
             'NCE Over': 0, 'NCE Under': 0, 'NCE F-measure': 0,
             'V Precision': 0, 'V Recall': 0, 'V-measure': 0}

    if TO_WRITE:
        file_all_scores = open(result_path + '/scores_goodlevel.txt', "w")
        csvfile_all_scores = open(result_path + '/scores_goodlevel.csv', 'w', newline='')
        csvwriter_all_scores = csv.writer(csvfile_all_scores, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    for i in range(min_val,max_val + 1):
        if i < 10:
            number = '0' + str(i)
        else:
            number = str(i)
        if i in tab_error:
            continue
        print("ANALYSIS NUMBER " + str(number))
        test_path_pop = test_path + '/Pop ' + number + ' (grid).csv'
        result_path_pop = result_path + '/Pop ' + number + '/'
        ref_labels, ref_intervals = rwcpp_ref.rwcpop_parse_ref_sec(test_path_pop)
        est_labels_all, est_intervals_all = rwcpp_est.rwcpop_parse_est(test_path_pop, result_path_pop)

        if TO_WRITE:
            if not os.path.exists(result_path_pop):
                os.makedirs(result_path_pop)
            file_scores = open(result_path_pop + "scores.txt", "w")
            csvfile_scores = open(result_path_pop + "scores.csv", 'w', newline='')
            csvwriter_scores = csv.writer(csvfile_scores, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        best_scores = 0
        best_scores_line = "no best score"
        best_level = 0

        for level in range(len(est_labels_all)):
            est_labels = est_labels_all[level]
            est_intervals = est_intervals_all[level]
            scores = mir_eval.segment.evaluate(ref_intervals, ref_labels, est_intervals, est_labels)
            # 'Pairwise F-measure' or
            # 'F-measure@0.5' or
            # 'Recall@0.5'
            if scores['F-measure@3.0'] > best_scores:
                best_scores = scores['F-measure@3.0']
                best_scores_line = scores
                best_level = level

            if TO_WRITE:
                file_scores.write("Scores at level" + str(level) + "\n")
                file_scores.write(str(scores) + "\n")
                if level == 0:
                    csvwriter_scores.writerow(['file number'] + ['level'] + [i for i,j in best_scores_line.items()])
                csvwriter_scores.writerow([number] + [level] + [round(j, 2) for i,j in best_scores_line.items()])
                # print(scores)

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
        file_all_scores.close()
        csvfile_all_scores.close()


rwcpop_compute_scores()