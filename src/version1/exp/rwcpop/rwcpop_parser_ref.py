import numpy as np
import rwcpop_parser as rwcparse

def rwcpop_list2section(poplist):
    section = []
    section_timer = np.zeros((len(poplist), 2))
    ext_char = ['(',')','/','|', '*', '~', "'", '#', '-']
    for i in range(10):
        ext_char.append(str(i))
    for row_id in range(len(poplist)):
        section_char_id = 0
        if len(poplist[row_id][0]) > 1:
            while poplist[row_id][0][section_char_id] in ext_char:
                section_char_id += 1
        section.append([poplist[row_id][0][section_char_id]])
        if row_id == 0:
            last_timer = 0
        else:
            last_timer = int(section_timer[row_id - 1, 1])
        section_timer[row_id, 0] = last_timer
        section_timer[row_id, 1] = last_timer + int(poplist[row_id][1])/2
    return section, section_timer


def rwcpop_list2barsection(poplist):
    # TODO: à implémenter
    section_mesure = []
    section_mesure_timer = np.zeros((len(poplist), 2))
    for row in poplist:
        section_mesure.append([])
        for bar_el in row[2:]:
            return 0

def rwcpop_parse_ref_sec(path):
    poplist = rwcparse.rwcpop_csv2list(path)
    ref_label, ref_interval = rwcpop_list2section(poplist)
    return ref_label, ref_interval

def test():
    file = rwcparse.Path(__file__).resolve()
    project_root = str(file.parents[2])
    test_path = project_root + '/../../data/rwcpop/Pop 01 (grid).csv'
    ref_label, ref_interval = rwcpop_parse_ref_sec(test_path)
    print(ref_label, ref_interval)