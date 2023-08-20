import parameters as prm
import matplotlib.pyplot as plt

def phases_init():
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


def phases_add_level():
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


def phases_add_element(level, new_mat, diff, time_t, cost):
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


def phases_pop_element(level):
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


def phases_print():
    print("all hypothesis = ", prm.hypo)
    print("NSNC hypothesis = ", prm.hypo1)
    print("NSC hypothesis = ", prm.hypo2)
    print("SNC hypothesis = ", prm.hypo3)
    print("SC hypothesis = ", prm.hypo4)
    print("hypothesis time = ", prm.hypo_time)

def phases_cost_diagram_perphase():
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


def phases_cost_diagram_perlevel():
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


# === SECONDARY PHASES


def sphases_computing(hypo_tab):
    secondary_phases = []
    for level in range(len(hypo_tab)):
        secondary_phases.append([])
        secondary_phases[level].append(0)
        for i in range(1, len(hypo_tab[level])):
            if hypo_tab[level][i - 1] == 1 and hypo_tab[level][i] == 1:
                secondary_phases[level].append(1)
            if hypo_tab[level][i - 1] == 1 and hypo_tab[level][i] == 2:
                secondary_phases[level].append(2)
            if hypo_tab[level][i - 1] == 1 and hypo_tab[level][i] == 3:
                secondary_phases[level].append(3)
            if hypo_tab[level][i - 1] == 1 and hypo_tab[level][i] == 4:
                secondary_phases[level].append(4)

            if hypo_tab[level][i - 1] == 2 and hypo_tab[level][i] == 1:
                secondary_phases[level].append(5)
            if hypo_tab[level][i - 1] == 2 and hypo_tab[level][i] == 2:
                secondary_phases[level].append(6)
            if hypo_tab[level][i - 1] == 2 and hypo_tab[level][i] == 3:
                secondary_phases[level].append(7)
            if hypo_tab[level][i - 1] == 2 and hypo_tab[level][i] == 4:
                secondary_phases[level].append(8)

            if hypo_tab[level][i - 1] == 3 and hypo_tab[level][i] == 1:
                secondary_phases[level].append(9)
            if hypo_tab[level][i - 1] == 3 and hypo_tab[level][i] == 2:
                secondary_phases[level].append(10)
            if hypo_tab[level][i - 1] == 3 and hypo_tab[level][i] == 3:
                secondary_phases[level].append(11)
            if hypo_tab[level][i - 1] == 3 and hypo_tab[level][i] == 4:
                secondary_phases[level].append(12)

            if hypo_tab[level][i - 1] == 4 and hypo_tab[level][i] == 1:
                secondary_phases[level].append(13)
            if hypo_tab[level][i - 1] == 4 and hypo_tab[level][i] == 2:
                secondary_phases[level].append(14)
            if hypo_tab[level][i - 1] == 4 and hypo_tab[level][i] == 3:
                secondary_phases[level].append(15)
            if hypo_tab[level][i - 1] == 4 and hypo_tab[level][i] == 4:
                secondary_phases[level].append(16)
    return secondary_phases

def cost_per_sphase(secondary_phases_tab, costs):
    sphases = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]

    for level in range(len(secondary_phases_tab)):
        for phase_less1 in range(len(sphases)):
            sphases[phase_less1].append([])
        for ind in range(len(secondary_phases_tab[level])):
            for phase_less1 in range(len(sphases)):
                if secondary_phases_tab[level][ind] == phase_less1 + 1:
                    sphases[phase_less1][level].append(costs[level][ind])
                else:
                    sphases[phase_less1][level].append(0)
    return sphases

def sphases_cost_diagram(secondary_phases_tab):
    for level in range(len(secondary_phases_tab)):
        plt.figure(figsize=(32, 20))
        plt.title("secondary cognitive phases at level " + str(level))
        plt.xlabel("time")
        plt.ylabel("type of secondary phase")
        plt.plot(prm.hypo_time[level], secondary_phases_tab[level], ":o",  linewidth=0.8, markersize=2,
                 label="sequence of secondary phase at level " + str(level))
        plt.legend()


def sphases_cost_diagram_perlevel(sphases):
    for level in range(len(sphases[0])):
        fig = plt.figure(figsize=(32, 20))
        ax = fig.add_subplot(111)
        plt.title("secondary cognitive phases at level " + str(level))
        plt.xlabel("time")
        plt.ylabel("cost")
        cm = plt.get_cmap('tab20')
        ax.set_prop_cycle(color=[cm(1.*i/16) for i in range(16)])
        for phase in range(len(sphases)):
            if phase < 4:
                string = '1'
            elif phase >= 4 and phase < 8:
                string = '2'
            elif phase >= 8 and phase < 12:
                string = '3'
            else:
                string = '4'
            if phase%4 == 0:
                string += '1'
            elif phase%4 == 1:
                string += '2'
            elif phase%4 == 2:
                string += '3'
            else:
                string += '4'

            plt.plot(prm.hypo_time[level], sphases[phase][level], ":o",  linewidth=0.8, markersize=2,
                         label="cost for secondary phase" + string)
        plt.legend()


def sphases_cost_diagram_perphase(sphases):
    for phase in range(len(sphases)):
        plt.figure(figsize=(32, 20))
        plt.title("secondary phase " + str(phase + 1))
        plt.xlabel("time")
        plt.ylabel("cost")
        for level in range(len(sphases[phase])):
            plt.plot(prm.hypo_time[level], sphases[phase][level], ":o",  linewidth=0.8, markersize=2,
                     label="cost for secondary phase" + str(phase + 1) + "at level " + str(level))
        plt.legend()