import csv
import sys
from pathlib import Path # if you haven't already done so

file = Path(__file__).resolve()
project_root = str(file.parents[1])

def DP_csv2list(path):
    with open(path, newline='') as csvfile:
        popreader = csv.reader(csvfile, delimiter=';', quotechar='"')
        poplist = list(popreader)
    return poplist


def list2timesection(list):
    section_temps = []
    for row in list:
        section_temps.append([])
        for bar_el in row[:]:
            els = bar_el.split(',')
            for i in range(len(els)):
                el = els[i]
                section_temps[-1].append(el[:])
    return section_temps

def flatten(t):
    f = [item for sublist in t for item in sublist]
    return [f]

def timesection_flatten(timesection):
    return flatten(timesection)

def flatten(t):
    """Flatten une liste de listes en une seule liste"""
    return [item for sublist in t for item in sublist]

def flattsec2acformat(tsec):
    """
    Transforme une liste flattenée en chaîne compressée.
    Chaque élément unique devient un symbole (lettre), les répétitions réutilisent le même symbole.
    """
    mapping = {}
    acformat = ''
    char = 96  # commence avant 'a'

    for chord in tsec:
        if chord not in mapping:
            char += 1
            mapping[chord] = chr(char)
        acformat += mapping[chord]

    print("acformat", acformat)
    print("mapping", mapping)
    return acformat



def parser(path):
    poplist = DP_csv2list(project_root + '/daft_punk/Something_about_us_DP.csv')
    time_section = list2timesection(poplist)
    flat_time_section = timesection_flatten(time_section)
    acformat = flattsec2acformat(flat_time_section)
    return acformat
