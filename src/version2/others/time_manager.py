import module_parameters.parameters as prm

def init_time():
    prm.time_tab = []

def time_add_level():
    prm.time_tab.append([])

def compute_time(level):
    if len(prm.time_tab[level]) > 0 and prm.ind_lvl0 == prm.time_tab[level][-1]:
        prm.time_tab[level].append(len(prm.phases[0]))
    else:
        prm.time_tab[level].append(prm.ind_lvl0)