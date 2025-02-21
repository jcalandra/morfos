from pathlib import Path

file = Path(__file__).resolve()
import numpy as np

def parse_ref(path):
    ref_interval = []
    ref_label = []
    with open(path, "r", encoding="utf-8") as f:
        for interval in f:
            interval = interval.rstrip().split("\t")
            ref_interval.append([int(interval[0]), int(interval[1])])
            ref_label.append([interval[2]])
    ref_interval = np.array(ref_interval)
    print("ref_interval = ", ref_interval)
    print("ref_label = ", ref_label)
    return ref_label, ref_interval

def test():
    project_root = str(file.parents[2])
    test_path = project_root + '/../../data/rwcpop/aist-chorus/RM-P001.CHORUS.TXT'
    ref_label, ref_interval = parse_ref(test_path)
    print("ref interval", ref_interval)
    print("ref label", ref_label)

#test()