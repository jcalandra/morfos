import parameters as prm
import matplotlib.pyplot as plt

def hypothesis_init():
    prm.lambda_0 = prm.gamma = prm.alpha = prm.delta = prm.beta = 0

    prm.hypo = []
    prm.hypo1 = []
    prm.hypo2 = []
    prm.hypo3 = []
    prm.hypo4 = []

    prm.hypo1_cost = []
    prm.hypo2_cost = []
    prm.hypo3_cost = []
    prm.hypo4_cost = []

    prm.hypo_time = []


def hypothesis_add_level():
    #time is in cost_time
    prm.hypo.append([])
    prm.hypo1.append([])
    prm.hypo2.append([])
    prm.hypo3.append([])
    prm.hypo4.append([])

    prm.hypo1_cost.append([])
    prm.hypo2_cost.append([])
    prm.hypo3_cost.append([])
    prm.hypo4_cost.append([])

    prm.hypo_time.append([])


def hypothesis_add_element(level, new_mat, diff, time_t, cost):
    if new_mat == 1 and diff == 0:
        prm.hypo[level].append(prm.NSNC)
        prm.hypo1[level].append(prm.hypo_value)
        prm.hypo2[level].append(0)
        prm.hypo3[level].append(0)
        prm.hypo4[level].append(0)

        prm.hypo1_cost[level].append(cost)
        prm.hypo2_cost[level].append(0)
        prm.hypo3_cost[level].append(0)
        prm.hypo4_cost[level].append(0)

    elif new_mat == 1 and diff == 1:
        prm.hypo[level].append(prm.NSC)
        prm.hypo1[level].append(0)
        prm.hypo2[level].append(prm.hypo_value)
        prm.hypo3[level].append(0)
        prm.hypo4[level].append(0)

        prm.hypo1_cost[level].append(0)
        prm.hypo2_cost[level].append(cost)
        prm.hypo3_cost[level].append(0)
        prm.hypo4_cost[level].append(0)

    elif new_mat == 0 and diff == 0:
        prm.hypo[level].append(prm.SNC)
        prm.hypo1[level].append(0)
        prm.hypo2[level].append(0)
        prm.hypo3[level].append(prm.hypo_value)
        prm.hypo4[level].append(0)

        prm.hypo1_cost[level].append(0)
        prm.hypo2_cost[level].append(0)
        prm.hypo3_cost[level].append(cost)
        prm.hypo4_cost[level].append(0)

    elif new_mat == 0 and diff == 1:
        prm.hypo[level].append(prm.SC)
        prm.hypo1[level].append(0)
        prm.hypo2[level].append(0)
        prm.hypo3[level].append(0)
        prm.hypo4[level].append(prm.hypo_value)

        prm.hypo1_cost[level].append(0)
        prm.hypo2_cost[level].append(0)
        prm.hypo3_cost[level].append(0)
        prm.hypo4_cost[level].append(cost)

    else:
        prm.hypo[level].append(0)
        prm.hypo1[level].append(0)
        prm.hypo2[level].append(0)
        prm.hypo3[level].append(0)
        prm.hypo4[level].append(0)
        prm.hypo1_cost[level].append(0)
        prm.hypo2_cost[level].append(0)
        prm.hypo3_cost[level].append(0)
        prm.hypo4_cost[level].append(0)
    prm.hypo_time[level].append(time_t)


def hypothesis_pop_element(level):
    prm.hypo[level].pop()
    prm.hypo1[level].pop()
    prm.hypo2[level].pop()
    prm.hypo3[level].pop()
    prm.hypo4[level].pop()

    prm.hypo1_cost[level].pop()
    prm.hypo2_cost[level].pop()
    prm.hypo3_cost[level].pop()
    prm.hypo4_cost[level].pop()

    prm.hypo_time[level].pop()


def hypothesis_print():
    print("all hypothesis = ", prm.hypo)
    print("NSNC hypothesis = ", prm.hypo1)
    print("NSC hypothesis = ", prm.hypo2)
    print("SNC hypothesis = ", prm.hypo3)
    print("SC hypothesis = ", prm.hypo4)
    print("hypothesis time = ", prm.hypo_time)

def hypothesis_cost_diagram_perphase():
    plt.figure(figsize=(32, 20))
    plt.title("phase 1")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.hypo_time[level], prm.hypo1_cost[level], ":o",  linewidth=0.8, markersize=2,
                 label="cost for phase 1 at level " + str(level))
    plt.legend()

    plt.figure(figsize=(32, 20))
    plt.title("phase 2")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.hypo_time[level], prm.hypo2_cost[level], ":o",  linewidth=0.8, markersize=2,
                 label="cost for phase 2 at level " + str(level))
    plt.legend()
    plt.figure(figsize=(32, 20))
    plt.title("phase 3")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.hypo_time[level], prm.hypo3_cost[level], ":o",  linewidth=0.8, markersize=2,
                 label="cost for phase 3 at level " + str(level))
    plt.legend()
    plt.figure(figsize=(32, 20))
    plt.title("phase 4")
    plt.xlabel("time")
    plt.ylabel("cost")
    for level in range(len(prm.cost_total_tab)):
        plt.plot(prm.hypo_time[level], prm.hypo4_cost[level], ":o",  linewidth=0.8, markersize=2,
                 label="cost for phase 4 at level " + str(level))
    plt.legend()


def hypothesis_cost_diagram_perlevel():
    for level in range(len(prm.cost_total_tab)):
        plt.figure(figsize=(32, 20))
        plt.title("cognitive phases at level " + str(level))
        plt.xlabel("time")
        plt.ylabel("cost")
        plt.plot(prm.hypo_time[level], prm.hypo1_cost[level], ":o",  linewidth=0.8, markersize=2,
                 label="cost for phase 1")
        plt.plot(prm.hypo_time[level], prm.hypo2_cost[level], ":o",  linewidth=0.8, markersize=2,
                 label="cost for phase 2")
        plt.plot(prm.hypo_time[level], prm.hypo3_cost[level], ":o",  linewidth=0.8, markersize=2,
                 label="cost for phase 3")
        plt.plot(prm.hypo_time[level], prm.hypo4_cost[level], ":o",  linewidth=0.8, markersize=2,
                 label="cost for phase 4")
        plt.legend()