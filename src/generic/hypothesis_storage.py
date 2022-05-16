import parameters as prm

def hypothesis_init():
    prm.lambda_0 = prm.gamma = prm.alpha = prm.delta = prm.beta = 0
    prm.hypo = []
    prm.hypo1 = []
    prm.hypo2 = []
    prm.hypo3 = []
    prm.hypo4 = []
    prm.hypo_time = []


def hypothesis_add_level():
    #time is in cost_time
    prm.hypo.append([])
    prm.hypo1.append([])
    prm.hypo2.append([])
    prm.hypo3.append([])
    prm.hypo4.append([])
    prm.hypo_time.append([])


def hypothesis_add_element(level, new_mat, diff, time_t):
    if new_mat == 1 and diff == 0:
        prm.hypo[level].append(prm.NSNC)
        prm.hypo1[level].append(prm.hypo_value)
        prm.hypo2[level].append(0)
        prm.hypo3[level].append(0)
        prm.hypo4[level].append(0)
    elif new_mat == 1 and diff == 1:
        prm.hypo[level].append(prm.NSC)
        prm.hypo1[level].append(0)
        prm.hypo2[level].append(prm.hypo_value)
        prm.hypo3[level].append(0)
        prm.hypo4[level].append(0)
    elif new_mat == 0 and diff == 0:
        prm.hypo[level].append(prm.SNC)
        prm.hypo1[level].append(0)
        prm.hypo2[level].append(0)
        prm.hypo3[level].append(prm.hypo_value)
        prm.hypo4[level].append(0)
    elif new_mat == 0 and diff == 1:
        prm.hypo[level].append(prm.SC)
        prm.hypo1[level].append(0)
        prm.hypo2[level].append(0)
        prm.hypo3[level].append(0)
        prm.hypo4[level].append(prm.hypo_value)
    else:
        prm.hypo[level].append(0)
        prm.hypo1[level].append(0)
        prm.hypo2[level].append(0)
        prm.hypo3[level].append(0)
        prm.hypo4[level].append(0)
    prm.hypo_time[level].append(time_t)


def hypothesis_pop_element(level):
    prm.hypo[level].pop()
    prm.hypo1[level].pop()
    prm.hypo2[level].pop()
    prm.hypo3[level].pop()
    prm.hypo4[level].pop()
    prm.hypo_time[level].pop()


def hypothesis_print():
    print("all hypothesis = ", prm.hypo)
    print("NSNC hypothesis = ", prm.hypo1)
    print("NSC hypothesis = ", prm.hypo2)
    print("SNC hypothesis = ", prm.hypo3)
    print("SC hypothesis = ", prm.hypo4)
    print("hypothesis time = ", prm.hypo_time)
