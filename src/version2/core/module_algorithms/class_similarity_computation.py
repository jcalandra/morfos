import class_similarity_rules_symb
import class_similarity_rules_sig as sim_sig
import class_similarity_rules_symb as sim_symb
from module_parameters import parameters
import class_object

# ==================================================== SIGNAL ==========================================================
MFCC_BIT = parameters.MFCC_BIT
FFT_BIT = parameters.FFT_BIT
CQT_BIT = parameters.CQT_BIT
processing = parameters.processing
letter_diff = parameters.LETTER_DIFF

rate = parameters.SR
nb_value = parameters.NB_VALUES

nb_notes = parameters.NB_NOTES
NPO = parameters.NOTES_PER_OCTAVE
fmin = parameters.NOTE_MIN

def _compute_signal_similarity_rep(obj_compared, actual_obj, mat=None, level=0):
    desc_compared = obj_compared[1].descriptors.mean_descriptors[0][0]
    actual_desc = actual_obj.concat_obj.descriptors.mean_descriptors[0][0]
    if parameters.DIFF_CONCORDANCE:
        sim_digit_label, sim_value = sim_sig.diff_concordance(desc_compared, actual_desc)
    elif parameters.EUCLID_DISTANCE:
        sim_digit_label, sim_value = sim_sig.euclid_distance(desc_compared, actual_desc)
    else:
        sim_digit_label, sim_value = sim_sig.diff_concordance(desc_compared, actual_desc)
    return sim_digit_label, sim_value

def _compute_symbol_similarity_rep(obj_compared, actual_obj, mat, level=0):
    string_compared = obj_compared[1].concat_labels
    actual_string = actual_obj.concat_obj.concat_labels
    if level == 0:
        actual_string = actual_string[-1]
    if parameters.STRICT_EQUALITY:
        sim_digit_label, sim_value = sim_symb.compute_strict_equality(string_compared, actual_string, mat, level)
    elif parameters.ALIGNMENT:
        sim_digit_label, sim_value = sim_symb.compute_alignment(string_compared, actual_string, mat, level)
    else:
        sim_digit_label, sim_value = sim_symb.compute_alignment(string_compared, actual_string, mat, level)
    return sim_digit_label, sim_value

def compute_signal_similarity_rep(obj_compared, actual_obj, mat=None, level=0):
    sim_digit_label_sig, sim_value_sig = _compute_signal_similarity_rep(obj_compared, actual_obj, mat, level)
    sim_digit_label_symb, sim_value_symb = _compute_signal_similarity_rep(obj_compared, actual_obj, mat, level)
    sim_value = (sim_value_sig + sim_value_symb)/2
    if sim_value - (level)*0 >= parameters.teta:
        sim_digit_label = 1
    else:
        sim_digit_label = 0
    return sim_digit_label, sim_value


def compute_symbol_similarity_rep(obj_compared, actual_obj, mat=None, level=0):
    #sim_digit_label_sig, sim_value_sig = _compute_signal_similarity_rep(obj_compared, actual_obj, mat, level)
    sim_digit_label_symb, sim_value_symb = _compute_signal_similarity_rep(obj_compared, actual_obj, mat, level)
    sim_value = sim_value_symb
    if sim_value >= parameters.teta:
        sim_digit_label = 1
    else:
        sim_digit_label = 0
    return sim_digit_label, sim_value


def _compute_signal_similarity(ms_oracle, level, obj_compared_ind, actual_obj_ind):
    if level == 0:
        obj_compared = ms_oracle.levels[level].objects[obj_compared_ind].descriptors
        actual_obj = ms_oracle.levels[level].objects[actual_obj_ind].descriptors
    else:
        label = ms_oracle.levels[level].oracle.data[obj_compared_ind + 1]
        obj_compared = ms_oracle.levels[level- 1].materials.history[label][1].descriptors
        actual_obj = ms_oracle.levels[level - 1].concat_obj.descriptors

    desc_compared = obj_compared.mean_descriptors[0][0]
    actual_desc = actual_obj.mean_descriptors[0][0]

    if parameters.DIFF_CONCORDANCE:
        sim_digit_label, sim_value = sim_sig.diff_concordance(desc_compared, actual_desc)
    elif parameters.EUCLID_DISTANCE:
        sim_digit_label, sim_value = sim_sig.euclid_distance(desc_compared, actual_desc)
    else:
        sim_digit_label, sim_value = sim_sig.diff_concordance(desc_compared, actual_desc)

    return sim_value


def _compute_symbol_similarity(ms_oracle, level, obj_compared_ind, actual_obj_ind):
    if level > 1:
        matrix = ms_oracle.levels[level - 2].materials.sim_matrix
    else:
        matrix = ms_oracle.matrix.sim_matrix
    if level == 0:
        obj_compared = ms_oracle.levels[level].objects[obj_compared_ind].label
        actual_obj = ms_oracle.levels[level].objects[actual_obj_ind].label
    else:
        label = ms_oracle.levels[level].oracle.data[obj_compared_ind + 1]
        obj_compared = ms_oracle.levels[level- 1].materials.history[label][1].concat_labels
        actual_obj = ms_oracle.levels[level - 1].concat_obj.concat_labels
    if parameters.STRICT_EQUALITY:
        #concat_obj = ms_oracle.levels[level].concat_obj.concat_labels
        sim_digit_label, sim_value = class_similarity_rules_symb.compute_strict_equality(obj_compared,
                                                             actual_obj, matrix, level)
    elif parameters.ALIGNMENT:
        sim_digit_label, sim_value = class_similarity_rules_symb.compute_alignment(
            obj_compared,
            actual_obj, matrix, level)
    else:
        sim_digit_label, sim_value = class_similarity_rules_symb.compute_alignment(
            obj_compared,
            actual_obj, matrix, level)
    return sim_value

def compute_signal_similarity(ms_oracle, level, obj_compared_ind, actual_obj_ind):
    sim_value_sig = _compute_signal_similarity(ms_oracle, level, obj_compared_ind, actual_obj_ind)
    sim_value_symb = _compute_signal_similarity(ms_oracle, level, obj_compared_ind, actual_obj_ind)
    sim_value = (sim_value_sig + sim_value_symb)/2
    return sim_value

def compute_symbol_similarity(ms_oracle, level, obj_compared_ind, actual_obj_ind):
    #sim_value_sig = _compute_signal_similarity(ms_oracle, level, obj_compared_ind, actual_obj_ind)
    sim_value_symb = _compute_signal_similarity(ms_oracle, level, obj_compared_ind, actual_obj_ind)
    sim_value = sim_value_symb
    return sim_value


def similarity(ms_oracle, level):
    actual_object_descriptor = class_object.Descriptors()
    actual_object_descriptor.copy(ms_oracle.levels[level - 1].concat_obj.descriptors)
    len_av = len(ms_oracle.levels[level - 1].materials.sim_matrix.labels)
    ms_oracle.levels[level].update_oracle(ms_oracle, level)
    len_ap = len(ms_oracle.levels[level - 1].materials.sim_matrix.labels)
    if len_av == 0 or len_ap > len_av:
        digit = 0
    else:
        digit = 1
        indice = ms_oracle.levels[level].oracle.data[-1]
        window = ms_oracle.levels[level - 1].concat_obj.concat_signal
        new_rep = ms_oracle.levels[level - 1].materials.history[indice][0]
        new_rep.update(window, new_rep.label, actual_object_descriptor)
        return new_rep, digit

    new_char = chr(letter_diff + ms_oracle.levels[level].oracle.data[-1])
    new_rep = class_object.ObjRep()
    new_rep.init(ms_oracle.levels[level].concat_obj.concat_signal, new_char, actual_object_descriptor)
    return new_rep, digit


def char_next_level_similarity(ms_oracle, level):
    """ The function compare the actual new structured string with structured strings already seen before. For now,
    the strings have to be the exact sames to be considered as similar. The history_next tab is modified according to
    the results and the new string of upper level new_char is returned."""
    new_rep, sim_digit = similarity(ms_oracle, level)

    # new_obj update
    new_signal = ms_oracle.levels[level - 1].concat_obj.concat_signal
    new_descriptors = ms_oracle.levels[level - 1].concat_obj.descriptors

    new_obj = class_object.Object()
    new_obj.update(new_rep.label, new_descriptors, new_signal, new_rep)
    ms_oracle.levels[level].oracle.objects.append(new_obj)

    if sim_digit:
        return [new_obj]

    # material.history update
    concat_rep = ms_oracle.levels[level - 1].concat_obj
    ms_oracle.levels[level - 1].materials.update_history(new_rep, concat_rep, new_rep.descriptors)
    return [new_obj]
