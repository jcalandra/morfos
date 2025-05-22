from criterias.module_segmentation import class_segmentation_rules_symb
from criterias.module_segmentation import class_segmentation_rules_sig
import module_parameters.parameters as prm
import random

class Rules:
    def  __init__(self):
        self.sigRules = SigRules()
        self.symbRules = SymbRules()

class SigRules:
    def __init__(self):
        if len(prm.SYMB_MRULES) != len(prm.SYMB_PRULES):
            raise("problème d'initialisation des règles")
        self.nb_rules = len(class_segmentation_rules_sig.sigRule_tab[0])
        self.mandatory_rules = prm.SIG_MRULES
        self.prohibitive_rules = prm.SIG_PRULES

        self.result=ResultTest()

    def getResult(self, ms_oracle, level):
        self.result=ResultTest()
        for r in range(len(self.mandatory_rules)):
            if self.mandatory_rules[r]:
                self.result.mandatory_tests.append(class_segmentation_rules_sig.sigRule_tab[0][r](ms_oracle, level))
            if self.prohibitive_rules[r]:
                self.result.prohibitive_tests.append(class_segmentation_rules_sig.sigRule_tab[1][r](ms_oracle, level))
        return self.result


class SymbRules:
    def __init__(self):
        if len(prm.SYMB_MRULES) != len(prm.SYMB_PRULES):
            raise("problème d'initialisation des règles")
        self.nb_rules = len(class_segmentation_rules_symb.symbRule_tab[0])
        self.mandatory_rules = prm.SYMB_MRULES
        self.prohibitive_rules = prm.SYMB_PRULES

        self.result=ResultTest()

    def getResult(self, ms_oracle, level):
        self.result=ResultTest()
        for r in range(len(self.mandatory_rules)):
            if self.mandatory_rules[r]:
                self.result.mandatory_tests.append(class_segmentation_rules_symb.symbRule_tab[0][r](ms_oracle, level))
            if self.prohibitive_rules[r]:
                self.result.prohibitive_tests.append(class_segmentation_rules_symb.symbRule_tab[1][r](ms_oracle, level))
        return self.result




class ResultTest:
    def __init__(self):
        self.mandatory_tests = []
        self.prohibitive_tests = []


def segmentation_test(ms_oracle, level, rules):
    if class_segmentation_rules_symb.rule_0_segmentation_rule(ms_oracle, level):
        bool = 1
    else:
        if prm.processing == "signal":
            bool =  segmentation_str(ms_oracle, level, rules.symbRules) or \
                    segmentation_audio(ms_oracle, level, rules.sigRules)
            #bool = segmentation_audio(ms_oracle, level, rules.sigRules)

        else:
            bool = segmentation_str(ms_oracle, level, rules.symbRules) #and segmentation_audio(ms_oracle, level, rules.symbRules)
    return bool

def segmentation_test_noseg(ms_oracle, level, rules):
    # calculer rule 1 et rule 2 pour avoir la valeur du cout
    class_segmentation_rules_symb.rule_1_similarity_word(ms_oracle, level)
    class_segmentation_rules_symb.rule_2_existing_object(ms_oracle, level)
    bool = 0
    return bool

def segmentation_test_allseg(ms_oracle, level, rules):
    class_segmentation_rules_symb.rule_1_similarity_word(ms_oracle, level)
    class_segmentation_rules_symb.rule_2_existing_object(ms_oracle, level)
    if ms_oracle.levels[level].concat_obj.nb > 0 :
        bool = 1
    else:
        bool = 0
    return bool

def segmentation_test_maxseg(ms_oracle, level, rules):
    class_segmentation_rules_symb.rule_1_similarity_word(ms_oracle, level)
    class_segmentation_rules_symb.rule_2_existing_object(ms_oracle, level)
    if ms_oracle.levels[level].concat_obj.nb == 2:
        bool = 1
    else:
        bool = 0
    return bool

def segmentation_test_random(ms_oracle, level, rules):
    class_segmentation_rules_symb.rule_1_similarity_word(ms_oracle, level)
    class_segmentation_rules_symb.rule_2_existing_object(ms_oracle, level)
    if ms_oracle.levels[level].concat_obj.nb > 0 :
        bool = round(random.random())
    else:
        bool = 0
    return bool

def segmentation_test_randomconstraint(ms_oracle, level, rules):
    class_segmentation_rules_symb.rule_1_similarity_word(ms_oracle, level)
    class_segmentation_rules_symb.rule_2_existing_object(ms_oracle, level)
    if ms_oracle.levels[level].concat_obj.nb > 1 and ms_oracle.levels[level].concat_obj.nb < 7 :
        bool = round(random.random())
    else:
        bool = 0
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