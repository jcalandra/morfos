from criterias.module_segmentation import class_segmentation_rules
from module_parameters.parameters import LETTER_DIFF
import parameters as prm


class Rules:
    def __init__(self):
        if len(prm.MRULES) != len(prm.PRULES):
            raise("problème d'initialisation des règles")
        self.nb_rules = len(class_segmentation_rules.rule_tab[0])
        self.mandatory_rules = prm.MRULES
        self.prohibitive_rules = prm.PRULES

        self.result=ResultTest()


    def getResult(self, ms_oracle, level):
        self.result=ResultTest()
        for r in range(len(self.mandatory_rules)):
            if self.mandatory_rules[r]:
                self.result.mandatory_tests.append(class_segmentation_rules.rule_tab[0][r]( ms_oracle, level))
            if self.prohibitive_rules[r]:
                self.result.prohibitive_tests.append(class_segmentation_rules.rule_tab[1][r]( ms_oracle, level))
        return self.result

class ResultTest:
    def __init__(self):
        self.mandatory_tests = []
        self.prohibitive_tests = []


def segmentation_test(ms_oracle, level, rules):
    bool = segmentation_str(ms_oracle, level, rules) and segmentation_audio(ms_oracle, level, rules)
    return bool


def segmentation_str(ms_oracle, level, rules):
    results = rules.getResult(ms_oracle, level)
    mbool = 0
    pbool = 1
    for i in results.mandatory_tests:
        if i:
            mbool = 1
    for i in results.prohibitive_tests:
        if i == 0:
            pbool = 0
    bool = mbool and pbool
    return bool

def segmentation_audio(ms_oracle, level, rules):
    return 1