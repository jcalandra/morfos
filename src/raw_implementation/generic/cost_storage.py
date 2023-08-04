from raw_implementation import parameters as prm
import matplotlib.pyplot as plt


# DATA UPDATE
def cost_oracle_init():
    prm.cost_0_init_tab = []
    prm.cost_1_nb_comparison_tab= []
    prm.cost_2_ext_forward_link_tab = []
    prm.cost_3_sfx_candidate_tab = []
    prm.cost_3b_complete_tab = []
    prm.cost_4_nb_comparison_rep_tab = []
    prm.cost_5_sfx_candidate_rep_tab = []
    prm.cost_6_nb_comparison_parcours_tab = []
    prm.cost_7_sfx_candidate_parcours_tab = []
    prm.cost_8_sfx_tab = []
    prm.cost_9_new_mat_tab = []
    prm.cost_10_update_mat_tab = []
    prm.cost_11_nb_comparison_update_tab = []
    prm.cost_12_cost_sfx_update_tab = []
    prm.cost_13_last_update_tab = []
    prm.cost_14_find_sfx_tab = []
    prm.cost_15_rep_tab = []
    prm.cost_16_parcours_tab = []
    prm.cost_17_fix_sfx_tab = []
    prm.cost_18_update_tab = []

    prm.cost_19_comparisons_tab = []
    prm.cost_20_sfx_candidates_tab = []
    prm.cost_21_statics_tab = []

    prm.cost_22_theoretical_tab = []
    prm.cost_23_theoretical_and_mat_tab = []

    prm.cost_24_total_wo_correct_tab = []
    prm.cost_25_total_wo_correct_w_update_tab = []

    prm.cost_total_tab = []
    prm.cost_total_sum = []
    prm.cost_time = []


def cost_oracle_add_level():
    prm.cost_0_init_tab.append([])
    prm.cost_1_nb_comparison_tab.append([])
    prm.cost_2_ext_forward_link_tab.append([])
    prm.cost_3_sfx_candidate_tab.append([])
    prm.cost_3b_complete_tab.append([])
    prm.cost_4_nb_comparison_rep_tab.append([])
    prm.cost_5_sfx_candidate_rep_tab.append([])
    prm.cost_6_nb_comparison_parcours_tab.append([])
    prm.cost_7_sfx_candidate_parcours_tab.append([])
    prm.cost_8_sfx_tab.append([])
    prm.cost_9_new_mat_tab.append([])
    prm.cost_10_update_mat_tab.append([])
    prm.cost_11_nb_comparison_update_tab.append([])
    prm.cost_12_cost_sfx_update_tab.append([])
    prm.cost_13_last_update_tab.append([])
    prm.cost_14_find_sfx_tab.append([])
    prm.cost_15_rep_tab.append([])
    prm.cost_16_parcours_tab.append([])
    prm.cost_17_fix_sfx_tab.append([])
    prm.cost_18_update_tab.append([])

    prm.cost_19_comparisons_tab.append([])
    prm.cost_20_sfx_candidates_tab.append([])
    prm.cost_21_statics_tab.append([])

    prm.cost_22_theoretical_tab.append([])
    prm.cost_23_theoretical_and_mat_tab.append([])

    prm.cost_24_total_wo_correct_tab.append([])
    prm.cost_25_total_wo_correct_w_update_tab.append([])
    prm.cost_total_tab.append([])
    prm.cost_total_sum.append([])

    prm.cost_time.append([])


def cost_oracle_add_level_init0():
    prm.cost_0_init_tab.append([0])
    prm.cost_1_nb_comparison_tab.append([0])
    prm.cost_2_ext_forward_link_tab.append([0])
    prm.cost_3_sfx_candidate_tab.append([0])
    prm.cost_3b_complete_tab.append([0])
    prm.cost_4_nb_comparison_rep_tab.append([0])
    prm.cost_5_sfx_candidate_rep_tab.append([0])
    prm.cost_6_nb_comparison_parcours_tab.append([0])
    prm.cost_7_sfx_candidate_parcours_tab.append([0])
    prm.cost_8_sfx_tab.append([0])
    prm.cost_9_new_mat_tab.append([0])
    prm.cost_10_update_mat_tab.append([0])
    prm.cost_11_nb_comparison_update_tab.append([0])
    prm.cost_12_cost_sfx_update_tab.append([0])
    prm.cost_13_last_update_tab.append([0])
    prm.cost_14_find_sfx_tab.append([0])
    prm.cost_15_rep_tab.append([0])
    prm.cost_16_parcours_tab.append([0])
    prm.cost_17_fix_sfx_tab.append([0])
    prm.cost_18_update_tab.append([0])

    prm.cost_19_comparisons_tab.append([0])
    prm.cost_20_sfx_candidates_tab.append([0])
    prm.cost_21_statics_tab.append([0])

    prm.cost_22_theoretical_tab.append([0])
    prm.cost_23_theoretical_and_mat_tab.append([0])

    prm.cost_24_total_wo_correct_tab.append([0])
    prm.cost_25_total_wo_correct_w_update_tab.append([0])
    prm.cost_total_tab.append([0])
    prm.cost_total_sum.append([0])

    prm.cost_time.append([0])


def cost_oracle_add_element(level, time):
    prm.cost_0_init_tab[level].append(prm.cost_0_init)
    prm.cost_1_nb_comparison_tab[level].append(prm.cost_1_nb_comparison)
    prm.cost_2_ext_forward_link_tab[level].append(prm.cost_2_ext_forward_link)
    prm.cost_3_sfx_candidate_tab[level].append(prm.cost_3_sfx_candidate)
    prm.cost_3b_complete_tab[level].append(prm.cost_3b_complete)
    prm.cost_4_nb_comparison_rep_tab[level].append(prm.cost_4_nb_comparison_rep)
    prm.cost_5_sfx_candidate_rep_tab[level].append(prm.cost_5_sfx_candidate_rep)
    prm.cost_6_nb_comparison_parcours_tab[level].append(prm.cost_6_nb_comparison_parcours)
    prm.cost_7_sfx_candidate_parcours_tab[level].append(prm.cost_7_sfx_candidate_parcours)
    prm.cost_8_sfx_tab[level].append(prm.cost_8_sfx)
    prm.cost_9_new_mat_tab[level].append(prm.cost_9_new_mat)
    prm.cost_10_update_mat_tab[level].append(prm.cost_10_update_mat)
    prm.cost_11_nb_comparison_update_tab[level].append(prm.cost_11_nb_comparison_update)
    prm.cost_12_cost_sfx_update_tab[level].append(prm.cost_12_cost_sfx_update)
    prm.cost_13_last_update_tab[level].append(prm.cost_13_last_update)
    prm.cost_14_find_sfx_tab[level].append(prm.cost_14_find_sfx)
    prm.cost_15_rep_tab[level].append(prm.cost_15_rep)
    prm.cost_16_parcours_tab[level].append(prm.cost_16_parcours)
    prm.cost_17_fix_sfx_tab[level].append(prm.cost_17_fix_sfx)
    prm.cost_18_update_tab[level].append(prm.cost_18_update)

    prm.cost_19_comparisons_tab[level].append(prm.cost_19_comparisons)
    prm.cost_20_sfx_candidates_tab[level].append(prm.cost_20_sfx_candidates)
    prm.cost_21_statics_tab[level].append(prm.cost_21_statics)

    prm.cost_22_theoretical_tab[level].append(prm.cost_22_theoretical)
    prm.cost_23_theoretical_and_mat_tab[level].append(prm.cost_23_theoretical_and_mat)

    prm.cost_24_total_wo_correct_tab[level].append(prm.cost_24_total_wo_correct)
    prm.cost_25_total_wo_correct_w_update_tab[level].append(prm.cost_25_total_wo_correct_w_update)
    prm.cost_total_tab[level].append(prm.cost_total)

    if len(prm.cost_total_sum[level]) == 0:
        tc_sum = prm.cost_total
    else:
        tc_sum = prm.cost_total_sum[level][len(prm.cost_total_sum[level]) - 1] + prm.cost_total
    prm.cost_total_sum[level].append(tc_sum)

    prm.cost_time[level].append(time)


def cost_general_init():
    prm.lambda_0 = prm.gamma = prm.alpha = prm.delta = prm.beta = 0
    prm.lambda_levels = []
    prm.lambda_sum = []
    prm.lambda_tab = [prm.lambda_0]
    prm.lambda_time = [0]
    prm.gamma_levels = []
    prm.gamma_sum = []
    prm.gamma_tab = [prm.gamma]
    prm.gamma_time = [0]
    prm.alpha_levels = []
    prm.alpha_sum = []
    prm.alpha_tab = [prm.alpha]
    prm.alpha_time = [0]
    prm.delta_levels = []
    prm.delta_sum = []
    prm.delta_tab = [prm.delta]
    prm.delta_time = [0]
    prm.beta_levels = []
    prm.beta_sum = []
    prm.beta_tab = [prm.beta]
    prm.beta_time = [0]


def cost_general_add_level():
    # time is in cost_time
    prm.lambda_levels.append([])
    prm.gamma_levels.append([])
    prm.alpha_levels.append([])
    prm.delta_levels.append([])
    prm.beta_levels.append([])

    prm.lambda_sum.append([])
    prm.gamma_sum.append([])
    prm.alpha_sum.append([])
    prm.delta_sum.append([])
    prm.beta_sum.append([])


# PRINT
def cost_oracle_print():
    print("cost_0_init_tab = ", prm.cost_0_init_tab)
    print("cost_1_nb_comparison_tab = ", prm.cost_1_nb_comparison_tab)
    print("cost_2_ext_forward_link_tab = ", prm.cost_2_ext_forward_link_tab)
    print("cost_3_sfx_candidate_tab", prm.cost_3_sfx_candidate_tab)
    print("cost_3b_complete_tab", prm.cost_3b_complete_tab)
    print("cost_4_nb_comparison_rep_tab", prm.cost_4_nb_comparison_rep_tab)
    print("cost_5_sfx_candidate_rep_tab", prm.cost_5_sfx_candidate_rep_tab)
    print("cost_7_sfx_candidate_parcours_tab", prm.cost_7_sfx_candidate_parcours_tab)
    print("cost_8_sfx_tab", prm.cost_8_sfx_tab)
    print("cost_9_new_mat_tab", prm.cost_9_new_mat_tab)
    print("cost_10_update_mat_tab", prm.cost_10_update_mat_tab)
    print("cost_11_nb_comparison_update_tab", prm.cost_11_nb_comparison_update_tab)
    print("cost_12_cost_sfx_update_tab", prm.cost_12_cost_sfx_update_tab)
    print("cost_13_last_update_tab", prm.cost_13_last_update_tab)
    print("\n")
    print("cost_14_find_sfx_tab", prm.cost_14_find_sfx_tab)
    print("cost_15_rep_tab", prm.cost_15_rep_tab)
    print("cost_16_parcours_tab", prm.cost_16_parcours_tab)
    print("cost_17_fix_sfx_tab", prm.cost_17_fix_sfx_tab)
    print("cost_18_update_tab", prm.cost_18_update_tab)
    print("\n")
    print("cost_19_comparisons_tab", prm.cost_19_comparisons_tab)
    print("cost_20_sfx_candidates_tab", prm.cost_20_sfx_candidates_tab)
    print("cost_21_statics_tab", prm.cost_21_statics_tab)
    print("\n")
    print("cost_22_theoretical_tab", prm.cost_22_theoretical_tab)
    print("cost_23_theoretical_and_mat_tab", prm.cost_23_theoretical_and_mat_tab)
    print("\n")
    print("cost_24_total_wo_correct_tab", prm.cost_24_total_wo_correct_tab)
    print("cost_25_total_wo_correct_w_update_tab", prm.cost_25_total_wo_correct_w_update_tab)
    print("\n")
    print("total_cost_tab = ", prm.cost_total_tab)
    print("total_cost_sum = ", prm.cost_total_sum)
    print("total_cost_time = ", prm.cost_time)


def cost_general_print():
    print("lambda = ", prm.lambda_0)
    print("gamma = ", prm.gamma)
    print("alpha = ", prm.alpha)
    print("delta = ", prm.delta)
    print("beta = ", prm.beta)
    print("\n")
    print("lambda_tab = ", prm.lambda_tab)
    print("lambda_time = ", prm.lambda_time)
    print("gamma_tab = ", prm.gamma_tab)
    print("gamma_time = ", prm.gamma_time)
    print("alpha_tab = ", prm.alpha_tab)
    print("alpha_time = ", prm.alpha_time)
    print("delta_tab = ", prm.delta_tab)
    print("delta_time = ", prm.delta_time)
    print("beta_tab = ", prm.beta_tab)
    print("beta_time = ", prm.beta_time)

    print("lambda_levels = ", prm.lambda_levels)
    print("lambda_sum = ", prm.lambda_sum)
    print("gamma_levels = ", prm.gamma_levels)
    print("gamma_sum = ", prm.gamma_sum)
    print("alpha_levels = ", prm.alpha_levels)
    print("alpha_sum = ", prm.alpha_sum)
    print("delta_levels = ", prm.delta_levels)
    print("delta_sum = ", prm.delta_sum)
    print("beta_levels = ", prm.beta_levels)
    print("beta_sum = ", prm.beta_sum)


# DIAGRAM
def cost_diagram(title, x_label, y_label, x_tab, y_tab):
    plt.figure(figsize=(32, 20))
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.plot(x_tab, y_tab)


def cost_oracle_diagram_all_levels():
    plt.figure(figsize=(32, 20))
    plt.title("cost 0: init")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_0_init_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 1: nb comparison")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_1_nb_comparison_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 2: external forward links")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_2_ext_forward_link_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 3: suffixe candidate")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_3_sfx_candidate_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 3b: complete")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_3b_complete_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 4: nb comparaison rep")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_4_nb_comparison_rep_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 5: suffixe candidate rep")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_5_sfx_candidate_rep_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 6:  nb comparaison parcours")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_6_nb_comparison_parcours_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 7: suffixe candidate parcours")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_7_sfx_candidate_parcours_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 8: suffixe")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_8_sfx_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 9: new mat")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_9_new_mat_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 10: update mat")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_10_update_mat_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 11: nb comparison update")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_11_nb_comparison_update_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 12: suffixe update")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_12_cost_sfx_update_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 13: last update")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_13_last_update_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 14: find suffix")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_14_find_sfx_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 15: rep computation")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_15_rep_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 16: incertitude computation")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_16_parcours_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 17: fix suffix")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_17_fix_sfx_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 18: update")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_18_update_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 19: all comparisons")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_19_comparisons_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 20: all sfx candidates")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_20_sfx_candidates_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 21: static variables")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_21_statics_tab[level], ":o", linewidth=0.8,
                 markersize=2, label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 22:theoretical costs")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_22_theoretical_tab[level], ":o", linewidth=0.8,
                 markersize=2, label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 23: theoretical + mat costs")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_23_theoretical_and_mat_tab[level], ":o", linewidth=0.8,
                 markersize=2, label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 24: total without corrections")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_24_total_wo_correct_tab[level], ":o", linewidth=0.8,
                 markersize=2, label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 25: total without added corrections (with sfx update)")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_25_total_wo_correct_w_update_tab[level], ":o", linewidth=0.8,
                 markersize=2, label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 26 : total")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_total_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()


def cost_general_diagram_all_levels():
    # levels
    plt.figure(figsize=(32, 20))
    plt.title("alpha levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.alpha_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("lambda levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.lambda_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))

    plt.legend()
    plt.figure(figsize=(32, 20))
    plt.title("delta levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.delta_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("gamma levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.gamma_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("beta levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.beta_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    # sum
    plt.figure(figsize=(32, 20))
    plt.title("alpha levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.alpha_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("lambda levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.lambda_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))

    plt.legend()
    plt.figure(figsize=(32, 20))
    plt.title("delta levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.delta_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("gamma levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.gamma_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("beta levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.beta_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()


def cost_general_diagram_all():
    plt.figure(figsize=(32, 20))
    plt.title("beta levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.lambda_time, prm.lambda_tab, ":o", linewidth=0.8, markersize=2)
    plt.figure(figsize=(32, 20))
    plt.title("gamma")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.gamma_time, prm.gamma_tab, ":o", linewidth=0.8, markersize=2)
    plt.figure(figsize=(32, 20))
    plt.title("alpha")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.alpha_time, prm.alpha_tab, ":o", linewidth=0.8, markersize=2)
    plt.figure(figsize=(32, 20))
    plt.title("delta")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.delta_time, prm.delta_tab, ":o", linewidth=0.8, markersize=2)
    plt.figure(figsize=(32, 20))
    plt.title("beta")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.beta_time, prm.beta_tab, ":o", linewidth=0.8, markersize=2)


def cost_general_diagram_allinone():
    plt.figure(figsize=(32, 20))
    plt.title("general costs")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.lambda_time, prm.lambda_tab, ":o", linewidth=0.8, markersize=2, label="lambda")
    # plt.plot(prm.gamma_time, prm.gamma_tab, label="gamma")
    plt.plot(prm.alpha_time, prm.alpha_tab, ":o", linewidth=0.8, markersize=2, label="alpha")
    plt.plot(prm.delta_time, prm.delta_tab, ":o", linewidth=0.8, markersize=2, label="delta")
    plt.plot(prm.beta_time, prm.beta_tab, ":o", linewidth=0.8, markersize=2, label="beta")
    plt.legend()


def cost_general_diagram_allinone_sum():
    plt.figure(figsize=(32, 20))
    plt.title("general costs sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.lambda_time, prm.lambda_sum, "o", label="lambda")
    # plt.plot(prm.gamma_time, prm.gamma_tab, label="gamma")
    plt.plot(prm.alpha_time, prm.alpha_sum, "o", label="alpha")
    plt.plot(prm.delta_time, prm.delta_sum, "o", label="delta")
    plt.plot(prm.beta_time, prm.beta_sum, "o", label="beta")
    plt.legend()


def cost_oracle_diagram_all_levels_whypothesis():
    plt.figure(figsize=(32, 20))
    plt.title("cost 0: init")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_0_init_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 1: nb comparison")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_1_nb_comparison_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 2: external forward links")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_2_ext_forward_link_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 3: suffixe candidate")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_3_sfx_candidate_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 3b: complete")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_3b_complete_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 4: nb comparaison rep")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_4_nb_comparison_rep_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 5: suffixe candidate rep")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_5_sfx_candidate_rep_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 6:  nb comparaison parcours")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_6_nb_comparison_parcours_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 7: suffixe candidate parcours")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_7_sfx_candidate_parcours_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 8: suffixe")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_8_sfx_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 9: new mat")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_9_new_mat_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 10: update mat")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_10_update_mat_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 11: nb comparison update")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_11_nb_comparison_update_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 12: suffixe update")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_12_cost_sfx_update_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 13: last update")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_13_last_update_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 14: find suffix")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_14_find_sfx_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 15: rep computation")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_15_rep_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 16: incertitude computation")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_16_parcours_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 17: fix suffix")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_17_fix_sfx_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 18: update")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_18_update_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 19: all comparisons")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_19_comparisons_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 20: all sfx candidates")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_20_sfx_candidates_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 21: static variables")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_21_statics_tab[level], ":o", linewidth=0.8,
                 markersize=2, label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 22:theoretical costs")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_22_theoretical_tab[level], ":o", linewidth=0.8,
                 markersize=2, label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 23: theoretical + mat costs")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_23_theoretical_and_mat_tab[level], ":o", linewidth=0.8,
                 markersize=2, label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 24: total without corrections")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_24_total_wo_correct_tab[level], ":o", linewidth=0.8,
                 markersize=2, label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 25: total without added corrections (with sfx update)")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_25_total_wo_correct_w_update_tab[level], ":o", linewidth=0.8,
                 markersize=2, label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("cost 26 : total")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.cost_total_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()


def cost_general_diagram_all_levels():
    # levels
    plt.figure(figsize=(32, 20))
    plt.title("alpha levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.alpha_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("lambda levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.lambda_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("delta levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.delta_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("gamma levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.gamma_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("beta levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.beta_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    # sum
    plt.figure(figsize=(32, 20))
    plt.title("alpha levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.alpha_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("lambda levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.lambda_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("delta levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.delta_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("gamma levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.gamma_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("beta levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.beta_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()



def cost_general_diagram_all_levels_whypothesis():
    # levels
    plt.figure(figsize=(32, 20))
    plt.title("alpha levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.alpha_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("lambda levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.lambda_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("delta levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.delta_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("gamma levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.gamma_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("beta levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.beta_levels[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    # sum
    plt.figure(figsize=(32, 20))
    plt.title("alpha levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.alpha_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("lambda levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.lambda_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("delta levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.delta_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("gamma levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.gamma_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("beta levels sum")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.cost_time[level], prm.beta_sum[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()


def cost_general_diagram_all_whypothesis():
    plt.figure(figsize=(32, 20))
    plt.title("beta levels")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.lambda_time, prm.lambda_tab, ":o", linewidth=0.8, markersize=2)
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("gamma")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.gamma_time, prm.gamma_tab, ":o", linewidth=0.8, markersize=2)
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("alpha")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.alpha_time, prm.alpha_tab, ":o", linewidth=0.8, markersize=2)
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("delta")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.delta_time, prm.delta_tab, ":o", linewidth=0.8, markersize=2)
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("beta")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.beta_time, prm.beta_tab, ":o", linewidth=0.8, markersize=2)
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()


def cost_general_diagram_allinone_whypothesis():
    plt.figure(figsize=(32, 20))
    plt.title("general costs")
    plt.xlabel("time")
    plt.ylabel("cost")
    plt.plot(prm.lambda_time, prm.lambda_tab, ":o", linewidth=0.8, markersize=2, label="lambda")
    # plt.plot(prm.gamma_time, prm.gamma_tab, label="gamma")
    plt.plot(prm.alpha_time, prm.alpha_tab, ":o", linewidth=0.8, markersize=2, label="alpha")
    plt.plot(prm.delta_time, prm.delta_tab, ":o", linewidth=0.8, markersize=2, label="delta")
    plt.plot(prm.beta_time, prm.beta_tab, ":o", linewidth=0.8, markersize=2, label="beta")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.hypo_time[level], prm.hypo[level], "o",  linewidth=0.8, markersize=2,
                 label="hypothesis at level " + str(level))
    plt.legend()