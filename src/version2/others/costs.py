import module_parameters.parameters as prm
import class_similarity_rules_symb as sim_symb
import matplotlib.pyplot as plt

global cost_organisation_sim
global cost_segmentation_sim
global cost_classification_sim

global cost_organisation_sim_tab
global cost_segmentation_sim_tab
global cost_classification_sim_tab
global cost_total_sim_tab

global cost_total_org_sim
global cost_total_seg_sim
global cost_total_class_sim
global cost_total_sim

global cost_total_sum_sim

global cost_organisation_op
global cost_segmentation_op
global cost_classification_op
global cost_total_op
global cost_total_sum_op

global total_len


## init costs

def init_cost():
    global cost_organisation_sim_tab
    global cost_segmentation_sim_tab
    global cost_classification_sim_tab
    global cost_total_sim_tab

    cost_organisation_sim_tab = []
    cost_segmentation_sim_tab = []
    cost_classification_sim_tab = []
    cost_total_sim_tab = []

    global cost_total_org_sim
    global cost_total_seg_sim
    global cost_total_class_sim
    global cost_total_sim

    cost_total_org_sim = 0
    cost_total_seg_sim = 0
    cost_total_class_sim = 0
    cost_total_sim = 0

    global cost_total_sum_sim
    global cost_total_sum_op

    cost_total_sum_sim = 0
    cost_total_sum_op = 0

    global total_len
    total_len = 0


def reinit_cost():
    global cost_organisation_sim
    global cost_segmentation_sim
    global cost_classification_sim
    global cost_total_sim

    cost_segmentation_sim = 0
    cost_classification_sim = 0
    cost_organisation_sim = 0
    cost_total_sim = 0


def costs_add_level():
    global cost_organisation_sim_tab
    global cost_segmentation_sim_tab
    global cost_classification_sim_tab
    global cost_total_sim_tab

    cost_organisation_sim_tab.append([])
    cost_segmentation_sim_tab.append([])
    cost_classification_sim_tab.append([])
    cost_total_sim_tab.append([])


## compute costs

def cost_compute_seg(ms_oracle, level): #TODO: @jcalandra 20/05/2025 loop for each voices
    global cost_segmentation_sim
    history_next = ms_oracle.levels[level].voices[0].VoiceMaterials.history
    actual_char = ms_oracle.levels[level].voices[0].actual_char
    concat_obj_lab = ms_oracle.levels[level].voices[0].concat_obj.extConcatNote.concatNote.concat_labels
    if level == 0:
        matrix = ms_oracle.matrix.sim_matrix
    else:
        matrix = ms_oracle.levels[level - 1].voices[0].VoiceMaterials.sim_matrix

    cost_seg_sim_1 = 0
    cost_seg_sim_2 = 0
    card_memory = len(history_next)

    for element in history_next:
        cost_seg_sim_1 += (1 - sim_symb.compute_alignment(chr(actual_char + prm.LETTER_DIFF), element[1].extConcatNote.concatNote.concat_labels[0], matrix)[1])
        cost_seg_sim_2 += (1 - sim_symb.compute_alignment(concat_obj_lab, element[1].extConcatNote.concatNote.concat_labels, matrix)[1])
    if card_memory == 0:
        cost_segmentation_sim = 0
    else:
        # cost_segmentation_sim = (cost_seg_sim_1 + cost_seg_sim_2)/(2*card_memory)
        cost_segmentation_sim = (cost_seg_sim_1 + cost_seg_sim_2)


def cost_compute_org(ms_oracle, level):
    global cost_organisation_sim
    actual_char = ms_oracle.levels[level].voices[0].actual_char
    concat_obj_lab = ms_oracle.levels[level].voices[0].concat_obj.extConcatNote.concatNote.concat_labels

    if level == 0:
        matrix = ms_oracle.matrix.sim_matrix
    else:
        matrix = ms_oracle.levels[level - 1].voices[0].VoiceMaterials.sim_matrix

    cost_org_sim = 0
    card_history = len(concat_obj_lab)
    for element in concat_obj_lab:
        # cost_org_sim += csc.compute_symbol_similarity_rep(chr(actual_char + prm.LETTER_DIFF), element, matrix, level)[1]
        cost_org_sim += (1-sim_symb.compute_alignment(chr(actual_char + prm.LETTER_DIFF), element, matrix)[1])
    if card_history == 0:
        cost_organisation_sim = 0
    else:
        cost_organisation_sim = cost_org_sim/card_history
        #cost_organisation_sim = cost_org_sim

# classification cost is directly computed within the oracle


def cost_compute_object_total():
    c = cost_classification_sim + cost_organisation_sim + cost_segmentation_sim
    return c


def cost_compute_total():
    global cost_total_sum_sim
    global cost_total_sim
    global total_len
    cost_total_sim = cost_compute_object_total()
    total_len += 1
    cost_total_sum_sim += cost_total_sim


def cost_compute_org_total():
    global cost_total_org_sim
    cost_total_org_sim += cost_organisation_sim


def cost_compute_seg_total():
    global cost_total_seg_sim
    cost_total_seg_sim += cost_segmentation_sim


def cost_compute_class_total():
    global cost_total_class_sim
    cost_total_class_sim += cost_classification_sim


def cost_compute_all_total():
    cost_compute_total()
    cost_compute_org_total()
    cost_compute_seg_total()
    cost_compute_class_total()


## add costs in tabs

def cost_organisation_add(level):
    global cost_organisation_sim_tab
    cost_organisation_sim_tab[level].append(cost_organisation_sim)

def cost_classification_add(level):
    global cost_classification_sim_tab
    cost_classification_sim_tab[level].append(cost_classification_sim)

def cost_segmentation_add(level):
    global cost_segmentation_sim_tab
    cost_segmentation_sim_tab[level].append(cost_segmentation_sim)

def cost_total_add(level):
    global cost_total_sim_tab
    cost_total_sim_tab[level].append(cost_total_sim)

def cost_add(level):
    cost_organisation_add(level)
    cost_classification_add(level)
    cost_segmentation_add(level)
    cost_total_add(level)


# main function

def compute_cost(ms_oracle, level):
    cost_compute_seg(ms_oracle, level)
    cost_compute_org(ms_oracle, level)
    cost_compute_all_total()
    cost_add(level)

    reinit_cost()

def normalise_cost():
    global cost_organisation_sim_tab
    global cost_segmentation_sim_tab
    global cost_classification_sim_tab
    global cost_total_sim_tab

    global cost_total_org_sim
    global cost_total_seg_sim
    global cost_total_class_sim
    global cost_total_sim

    global cost_total_sum_sim

    '''cost_organisation_sim_tab /= total_len
    cost_segmentation_sim_tab /= total_len
    cost_classification_sim_tab /= total_len
    cost_total_sim_tab /= total_len'''

    cost_total_org_sim /= total_len
    cost_total_seg_sim /= total_len
    cost_total_class_sim /= total_len
    cost_total_sim /= total_len

    cost_total_sum_sim /= total_len

# print costs

def print_cost():
    print("total :",cost_total_sum_sim)
    print("len", total_len)
    print("\n")
    print("organisation :",cost_total_org_sim)
    print("classification :", cost_total_class_sim)
    print("segmentation :", cost_total_seg_sim)
    print("\n")
    print("organisation tab :", cost_organisation_sim_tab)
    print("classification tab :", cost_classification_sim_tab)
    print("segmentation tab :", cost_segmentation_sim_tab)
    print("total tab :", cost_total_sim_tab)
    print("time :", prm.time_tab)

def save_cost():
    file_name = "info.txt"
    file = open(prm.PATH_RESULT + file_name , "a")
    file.write("total :" + str(cost_total_sum_sim) + "\n")
    file.write("len" + str(total_len) + "\n")
    file.write("\n")
    file.write("organisation :" + str(cost_total_org_sim) + "\n")
    file.write("classification :" + str(cost_total_class_sim) + "\n")
    file.write("segmentation :" + str(cost_total_seg_sim) + "\n")
    file.write("\n")
    file.write("organisation tab :" + str(cost_organisation_sim_tab) + "\n")
    file.write("classification tab :" + str(cost_classification_sim_tab) + "\n")
    file.write("segmentation tab :" + str(cost_segmentation_sim_tab) + "\n")
    file.write("total tab :" + str(cost_total_sim_tab) + "\n")
    file.write("time :" + str(prm.time_tab) + "\n")

    file.close()

def save_main_cost():
    file_name = "main_info.txt"
    file = open(prm.PATH_RESULT + file_name , "a")
    file.write(str(cost_total_sum_sim) + ";")
    file.write(str(cost_total_org_sim) + ";")
    file.write(str(cost_total_class_sim) + ";")
    file.write(str(cost_total_seg_sim) + ";")
    file.write(str(total_len) + "\n")
    file.close()

# print diagrams
def cost_general_diagram_all_levels():
    # levels
    plt.figure(figsize=(16, 10))
    plt.title("total cost per object")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(cost_total_sim_tab)):
        plt.plot(prm.time_tab[level], cost_total_sim_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()
    file_name_pyplot = "totalcost.png"
    plt.savefig(prm.PATH_RESULT + file_name_pyplot, transparent=True, dpi=1000)

    plt.figure(figsize=(16, 10))
    plt.title("organisation cost per object")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(cost_organisation_sim_tab)):
        plt.plot(prm.time_tab[level], cost_organisation_sim_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()
    file_name_pyplot = "organisationcost.png"
    plt.savefig(prm.PATH_RESULT + file_name_pyplot, transparent=True, dpi=1000)

    plt.figure(figsize=(16, 10))
    plt.title("classification cost per object")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(cost_classification_sim_tab)):
        plt.plot(prm.time_tab[level], cost_classification_sim_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()
    file_name_pyplot = "classificationcost.png"
    plt.savefig(prm.PATH_RESULT + file_name_pyplot, transparent=True, dpi=1000)

    plt.figure(figsize=(16, 10))
    plt.title("segmentation cost per object")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(cost_segmentation_sim_tab)):
        plt.plot(prm.time_tab[level], cost_segmentation_sim_tab[level], ":o", linewidth=0.8, markersize=2,
                 label="level " + str(level))
    plt.legend()
    file_name_pyplot = "segmentationcost.png"
    plt.savefig(prm.PATH_RESULT + file_name_pyplot, transparent=True, dpi=1000)