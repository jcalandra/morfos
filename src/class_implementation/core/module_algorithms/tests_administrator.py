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


########################################### old
def rules_parametrization(ms_oracle, level):
    """ Structuring test function: if one test is validated, there is structuration."""
    if class_segmentation_rules.RULE_1:
        test_1 = class_segmentation_rules.rule_1_similarity_word(ms_oracle, level)
    else:
        test_1 = 1
    if class_segmentation_rules.RULE_3:
        test_3 = class_segmentation_rules.rule_3_recomputed_object(ms_oracle, level)
    else:
        test_3 = 0
    if class_segmentation_rules.RULE_4:
        test_4 = class_segmentation_rules.rule_4_not_validated_hypothesis(ms_oracle, level)
    else:
        test_4 = 1
    if not class_segmentation_rules.RULE_1 and not class_segmentation_rules.RULE_4:
        test_1 = 0
        test_4 = 0
    if class_segmentation_rules.RULE_2 and test_3 == 0:
        test_2 = class_segmentation_rules.rule_2_existing_object(ms_oracle, level)
    else:
        test_2 = 0
    if class_segmentation_rules.RULE_5:
        test_5 = class_segmentation_rules.rule_5_regathering_after(ms_oracle, level)
    else:
        test_5 = 1

    if test_3:
        label_data = [ord(ms_oracle.levels[level].objects[i].label) - LETTER_DIFF
                      for i in range(len(ms_oracle.levels[level].objects))]

        ms_oracle.levels[level].iterator = len(ms_oracle.levels[level].concat_obj.concat_labels)
        ms_oracle.levels[level].shift = len(ms_oracle.levels[level].oracle.data) - len(
            ms_oracle.levels[level].concat_obj.concat_labels) - 1
        ms_oracle.levels[level].update_oracle(label_data[ms_oracle.levels[level].iterator + ms_oracle.levels[level].shift])
        ms_oracle.levels[level].actual_char = \
            ms_oracle.levels[level].oracle.data[ms_oracle.levels[level].shift + ms_oracle.levels[level].iterator + 1]
        ms_oracle.levels[level].data_length = len(ms_oracle.levels[level].formal_diagram.material_lines[0])
        ms_oracle.levels[level].objects = ms_oracle.levels[level].objects[ms_oracle.levels[level].shift:]

        ms_oracle.levels[level].formal_diagram.update(ms_oracle, level)
        ms_oracle.levels[level].formal_diagram_graph.update(ms_oracle, level)

        for i in range(len(ms_oracle.levels)):
            print(ms_oracle.levels[i].oracle.data)

        print("label_data", label_data)
        print("label iterator", ms_oracle.levels[level].iterator)
        print("label shift", ms_oracle.levels[level].shift)

    return test_1, test_2, test_3, test_4, test_5