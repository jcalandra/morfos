import matplotlib.pyplot as plt
import parameters as prm

# In this file are implemented the rules that give segmentation criteria, without the Oracle (nor alignement techniques)
# The similarity test function (char_next_level_similarity) and main algorithm are implemented in this file too (the
# segmentation test function is in the main algorithm).
# Functions for the creations of the formal diagrams from strings are provided.
# Exemples from strings are provided at the end of this file
# Remarque: ce fichier est probablement voué à être supprimé

# ================================================= RULES ==============================================================
# 5 rules are proposed :
# RULE_1 : there is a structuration if the actual object has already be seen in the same level of structure.
# RULE_2 : there is no structuration if an hypothesis about the upper level is validated.  RULE_2 is actually the
# opposite of this rule, meaning that there is structuration if any hypothesis is validated.
# RULE_3 : There is structuration on this level if the concatenated object is an object already seen on the upper level.
# RULE_4 : RULE_4 is the same rule as RULE_3 except that it takes account of precedently unachieved objects that are
# seen again and have then to be modified such as it become an object of upper level.
# RULE_5 : A structured object of upper level wich is alone is gathered with the next group.
# On the extern parameters, 1 means that the rule is applied and 0 means that the rule is not applied.

RULE_1 = prm.RULE_1
RULE_2 = prm.RULE_2
RULE_3 = prm.RULE_3
RULE_4 = prm.RULE_4
RULE_5 = prm.RULE_5


def rule_1_similarity(history, actual_char):
    """ Compare the actual char which is analysed actual_char with all objects that are already seen in the actual level
    and stocked in the tab history[]. Return 1 if the actual_char has already been seen, otherwise the function appends
    it to the history tab and returns 0."""
    for i in range(len(history)):
        if actual_char == history[i]:
            return 1
    history.append(actual_char)
    return 0


# The function is developed without the Factor Oracle. The Factor oracle would induce faster computing.
def validated_hypothesis(history_next, concat_obj, actual_char):
    """ Compare the concatenated object concat_obj of unstructured char in the actual level plus the actual_char, with
    the already seen objects in the past that begins with the same concat_obj. If the strings are equals, hypothesis
     from the past are validated and there should be no structuration right now because this is middle of the creation
     of an already known object of upper level. The function returns 1 then, 0 otherwise."""
    for i in range(len(history_next)):
        for j in range(len(history_next[i][1])):
            crop_car = str(history_next[i][1][j:j + len(concat_obj + actual_char)])
            if crop_car == concat_obj + actual_char:
                return 1
    return 0


def rule_2_not_validated_hypothesis(history_next, concat_obj, actual_char):
    """ This function compute the previous function validated hypothesis and returns the opposite result."""
    return abs(1 - validated_hypothesis(history_next, concat_obj, actual_char))


def rule_3_existing_object(history_next, concat_obj):
    """ This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with objects of the upper level stocked in the tab history_next[]. If the strings are similar, returns 1. Otherwise
    the function returns 0."""
    for i in range(len(history_next)):
        if history_next[i][1] == concat_obj:
            return 1
    return 0


# The function is developed without the Factor Oracle. The Factor oracle would induce faster computing.
def rule_4_recomputed_object(structured_char, new_char, history_next, concat_obj, actual_char):
    """ This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with substrings of objects of the upper level stocked in the tab history_next[]. If the strings are similar, the
    structures structured_char, new_char and history_next has to be modify in consequences such as the substring become
    an entire object of upper level. If the function find similar strings, it returns the new new_char, otherwise it
    returns 0."""
    # Comparisons between concat_obj and substrings of history_next.
    if len(concat_obj) == 1:
        return 0
    for i in range(len(history_next)):
        for j in range(len(history_next[i][1])):
            crop_car = str(history_next[i][1][j:j + len(concat_obj)])
            if crop_car == concat_obj \
                    and len(crop_car) < len(history_next[i][1]) \
                    and (j + len(concat_obj) == len(history_next[i][1])
                         or str(history_next[i][1][j + len(concat_obj)]) != actual_char):

                # If a former substring is found, the structured_char, history_next and new_char are modified such as
                # the substring is an object of upper level.
                structure_k = -1
                for ind in range(len(structured_char)):
                    if history_next[i][1] == structured_char[ind]:
                        structure_k = ind

                temp_obj = history_next[i]
                history_next.pop(i)
                structured_char.pop(structure_k)

                history_k = i
                leter = ord(temp_obj[0])
                if j > 0:
                    new_el = (temp_obj[0], temp_obj[1][0:j])
                    history_next.insert(history_k, new_el)
                    structured_char.insert(structure_k, temp_obj[1][0:j])
                    history_k += 1
                    structure_k += 1
                    leter = leter + 1
                new_el = (chr(leter), temp_obj[1][j:j + len(concat_obj)])
                history_next.insert(history_k, new_el)
                structured_char.insert(structure_k, temp_obj[1][j:j + len(concat_obj)])
                history_k += 1
                structure_k += 1
                leter = leter + 1
                if j + len(concat_obj) < len(temp_obj[1]):
                    new_el = (chr(leter), temp_obj[1][j + len(concat_obj):])
                    history_next.insert(history_k, new_el)
                    structured_char.insert(structure_k, temp_obj[1][j + len(concat_obj):])
                    history_k += 1
                    structure_k += 1
                    leter = leter + 1
                for ind in range(history_k, len(history_next)):
                    new_el = (chr(leter), history_next[ind][1])
                    history_next[ind] = new_el
                    leter = leter + 1

                diff = abs(history_k - 1 - i)
                for ind in range(structure_k - diff + 1, len(new_char)):
                    if new_char[ind] > temp_obj[0]:
                        new_char = new_char[:ind] + chr(ord(new_char[ind]) + diff) + new_char[ind + 1:]

                leter = ord(temp_obj[0]) + diff
                for ind2 in range(diff):
                    new_char = new_char[:structure_k + 1] + chr(leter) + new_char[structure_k + 1:]
                    leter = leter - 1
                return new_char
    return 0


def rule_5_regathering(concat_obj):
    """ The function returns 1 if the length of the string corresponding to  the concatenated object that are not
    structured in the actual level is higher than one. It returns 0 if the length of the string is equal or less than
    one."""
    if len(concat_obj) > 1:
        return 1
    return 0


# ======================================== SIMILARITY TEST FUNCTION ====================================================
def char_next_level_similarity(new_char, history_next, structured_char, concat_obj):
    """ The function compare the actual new structured string with structured strings already seen before. For now,
    the strings have to be the exact sames to be considered as similar. The history_next tab is modified according to
    the results and the new string of upper level new_char is returned."""
    for i in range(len(structured_char)):
        if len(concat_obj) == len(structured_char[i]):
            j = 0
            while structured_char[i][j] == concat_obj[j]:
                j = j + 1
                if j == len(structured_char[i]):
                    new_char = new_char + (new_char[i])
                    return new_char
    new_char = new_char + (chr(97+len(history_next)))
    history_next.append((chr(97+len(history_next)), concat_obj))
    return new_char


# ======================================= MAIN COGNITIVE ALGORITHM FROM STRINGS ========================================
# For now, the implementation is with strings, and every function fun_segmentation is called once the former execution
# of this function is done.
def fun_segmentation(char):
    """This function browses the string char and structure it at the upper level according to the rules that are applied
    by the extern user. It returns the structured char which is a tab of substring representing upper level object, the
    new string wew_char of upper level with adequated letters and the tab history[] of objects that are seen in this
    level."""
    # Initalisation of the structures
    structured_char = []  # actual char structured in packages
    new_char = ''  # corresponding leters in the next level of hyerarchy
    history = []  # already seen chars in the actual level
    history_next = []  # already seen chars in the next level
    concat_obj = ''

    # Every new caracter is analysed.
    for i in range(len(char)):
        actual_char = char[i]  # i_th parsed caracter

        # First is the parametrisation of the rules according to the externs settings.
        if RULE_1:
            test_1 = rule_1_similarity(history, actual_char)
        else:
            test_1 = 1
        if RULE_2:
            test_2 = rule_2_not_validated_hypothesis(history_next, concat_obj, actual_char)
        else:
            test_2 = 1
        if not RULE_1 and not RULE_2:
            test_1 = 0
            test_2 = 0
        if RULE_4:
            test_4 = (rule_4_recomputed_object(structured_char, new_char, history_next, concat_obj, actual_char))
            if test_4 != 0:
                new_char = test_4
                test_4 = 1
        else:
            test_4 = 0
        if RULE_3:
            test_3 = rule_3_existing_object(history_next, concat_obj)
        else:
            test_3 = 0
        if RULE_5:
            test_5 = rule_5_regathering(concat_obj)
        else:
            test_5 = 1

        # If the tests are positives, there is structuration.
        if ((test_1 and test_2) or test_3 or test_4) and test_5:
            # Labelisation of upper level string and update of the differents structures
            new_char = char_next_level_similarity(new_char, history_next, structured_char, concat_obj)
            structured_char.append(concat_obj)
            # Envoyer ici au FO de niveau sup le noeud correspondant à concat_obj
            concat_obj = ''
        concat_obj = concat_obj + actual_char

        # If this is the End of String, there is automatically structuration
        if i == len(char) - 1:
            new_char = char_next_level_similarity(new_char, history_next, structured_char, concat_obj)
            structured_char.append(concat_obj)

    return structured_char, new_char, history, history_next


def algo_cog(char):
    """ This function creates the matrix that represents the formal diagram produce by the adequated string char. It
    returns the matrix corresponding to the formal diagram and the len of the string."""
    nb_mat = 1
    new_mat = [1 for i in range(len(char))]
    mtx = [new_mat]
    mtx[0][0] = 0
    for i_hop in range(1, len(char)):
        j_mat = ord(char[i_hop]) - 97
        if j_mat > len(mtx) - 1:
            nb_mat = nb_mat + 1
            new_mat = [1 for i in range(len(char))]
            mtx.append(new_mat)
            mtx[nb_mat - 1][i_hop] = 0
        else:
            mtx[j_mat][i_hop] = 0
    return mtx, len(char)


def graph_algo_cogn(char, matrix, data_duration_in_s):
    """ plot the picture of formal diagram matrix according to its length data_duration_in_s. The picture is named ofter the
    string char."""
    name = char
    plt.figure(figsize=(15, 5))
    plt.title("Diagramme formel de " + name)
    plt.gray()
    plt.imshow(matrix, extent=[0, data_duration_in_s, len(matrix), 0])
    plt.show()

# ================================================= EXEMPLES ===========================================================
# Here is a simple exemple with the analysis of a single string 'abacabacdeabfgabachijklmhinopqabacrsrsttu'
def example():
    char_ex = 'abacabacdeabfgabachijklmhinopqabacrsrsttu'
    structured_result, new_char_ex, history, history_next = fun_segmentation(char_ex)
    print("structuration of " + char_ex + " is : " + str(structured_result))
    print("History of materials :", history)
    print("History of upper level materials :", history_next)
    print("At next level, it gives the caracter string : " + new_char_ex)


# Here is a loop exemple where every formal diagram and according structures are produced until we can not structure
# anymore.  The conditions to stop the loop are :
# - either the size of the final object is one.
# - either we can not structure, meaning that the upper level is the same as the actual level.
def example_loop():
    char_ex = 'abacabacdeabfgabachijklmhinopqabacrsrsttu'
    mtx, char_length = algo_cog(char_ex)
    graph_algo_cogn(char_ex, mtx, char_length)
    old_char_ex = ''
    while len(char_ex) > 1 and old_char_ex != char_ex:
        old_char_ex = char_ex
        structured_result, char_ex, history, history_next = fun_segmentation(char_ex)
        print("structuration of '" + old_char_ex + "' is : " + str(structured_result))
        print("History of materials :", history)
        print("History of upper level materials :", history_next)
        print("At next level, it gives the caracter string : " + char_ex + "\n")
        mtx, char_length = algo_cog(char_ex)
        graph_algo_cogn(char_ex, mtx, char_length)


example_loop()
