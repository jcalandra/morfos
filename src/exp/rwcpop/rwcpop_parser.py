import csv
import sys
from pathlib import Path # if you haven't already done so

file = Path(__file__).resolve()
project_root = str(file.parents[1])

def rwcpop_csv2list(path):
    print("path", path)
    with open(path, newline='') as csvfile:
        popreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        poplist = list(popreader)
    return poplist


def rwcpop_list2timesection(list):
    section_temps = []
    for row in list:
        section_temps.append([])
        for bar_el in row[2:]:
            els = bar_el.split(',')
            for i in range(len(els)):
                el = els[i]
                if len(el) == 0 or el[0] == "[":
                    break
                if len(els) == 3 or len(els) == 4:
                    if el[0] == "(" and el[1:] != '%':
                        section_temps[-1].append(el[1:])
                    elif el[-1] == ")" and el[:-1] != '%':
                        section_temps[-1].append(el[:-1])
                    else:
                        not_percent = 1
                        for i in range(len(el)):
                            if  el[i] == '%':
                                not_percent = 0
                        if not_percent:
                            section_temps[-1].append(el)
                            section_temps[-1].append(el)
                if len(els) == 2 and el != '%':
                    section_temps[-1].append(el)
                    section_temps[-1].append(el)
                if len(els) == 1 and el != '%':
                    section_temps[-1].append(el)
                    section_temps[-1].append(el)
                    section_temps[-1].append(el)
                    section_temps[-1].append(el)
    return section_temps

def flatten(t):
    return [item for sublist in t for item in sublist]

def timesection_flatten(timesection):
    return flatten(timesection)

def flattsec2acformat(tsec):
    dict = {}
    acformat = ''
    char = 96
    for chord in tsec:
        if chord in dict:
            acformat += dict[chord]
        else:
            char += 1
            dict[chord] = chr(char)
            acformat += dict[chord]
    return acformat

def parser(path):
    poplist = rwcpop_csv2list(path)
    time_section = rwcpop_list2timesection(poplist)
    flat_time_section = timesection_flatten(time_section)
    acformat = flattsec2acformat(flat_time_section)
    return acformat

# parser(test_path)