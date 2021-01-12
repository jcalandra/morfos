import matplotlib.pyplot as plt
import oracle_ac

letter_diff = 96
# ================================================= RULES ==============================================================

# 5 rules are proposed :
# RULE_1 : Structuring if the actual object has already be seen in the same level of structure.
# RULE_2 : There is no structuring if an hypothesis about the upper level is validated.  RULE_2 is actually the
# opposite of this rule, meaning that there is structuring if any hypothesis is validated.
# RULE_3 : Structuring on this level if the concatenated object is an object already seen on the upper level.
# RULE_4 : RULE_4 is the same rule as RULE_3 except that it takes account of previously unfinished objects that are
# seen again and have then to be modified such as it become an object of upper level.
# RULE_5 : A structured object of upper level which is alone is gathered with the next group.
# On the external parameters, 1 means that the rule is applied and 0 means that the rule is not applied.

RULE_1 = 1
RULE_2 = 1
RULE_3 = 1
RULE_4 = 1
RULE_5 = 1


def rule_1_similarity(f_oracle, actual_char_ind):
    """ Compare the actual char which is analysed actual_char with all objects that are already seen in the actual level
    and stocked in the tab history[]. Return 1 if the actual_char has already been seen, otherwise the function appends
    it to the history tab and returns 0."""
    if f_oracle.sfx[actual_char_ind] != 0:
        return 1
    return 0


# The function is developed without the Factor Oracle. The Factor oracle would induce faster computing.
def validated_hypothesis(f_oracle, link, actual_char, actual_char_ind):
    """ Compare the concatenated object concat_obj of unstructured char in the actual level plus the actual_char, with
    the already seen objects in the past that begins with the same concat_obj. If the strings are equals, hypothesis
     from the past are validated and there should be no structuration right now because this is middle of the creation
     of an already known object of upper level. The function returns 1 then, 0 otherwise."""
    if len(f_oracle.data) > 2 and f_oracle.sfx[actual_char_ind - 1] != 0 \
            and f_oracle.data[f_oracle.sfx[actual_char_ind - 1] + 1] == actual_char \
            and link[f_oracle.sfx[actual_char_ind - 1]] == link[f_oracle.sfx[actual_char_ind - 1] + 1]:
        return 1
    return 0


def rule_2_not_validated_hypothesis(f_oracle, link, actual_char, actual_char_ind):
    """ This function compute the previous function validated hypothesis and returns the opposite result."""
    return abs(1 - validated_hypothesis(f_oracle, link, actual_char, actual_char_ind))


def rule_3_existing_object(history_next, concat_obj):
    """ This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with objects of the upper level stocked in the tab history_next[]. If the strings are similar, returns 1. Otherwise
    the function returns 0."""
    for i in range(len(history_next)):
        if history_next[i][1] == concat_obj:
            return 1
    return 0


# The function is developed without the Factor Oracle. The Factor oracle would induce faster computing.
def rule_4_recomputed_object_old(oracles, level, data_length, actual_char_ind):
    """ This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with substrings of objects of the upper level stocked in the tab history_next[]. If the strings are similar, the
    structures structured_char, new_char and history_next has to be modify in consequences such as the substring become
    an entire object of upper level. If the function find similar strings, it returns the new new_char, otherwise it
    returns 0."""
    # allocation of structures of actual level
    f_oracle = oracles[1][level][0]
    link = oracles[1][level][1]
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    nb_elements = len(concat_obj)

    # Comparisons between concat_obj and the string starting from the suffix of the first char of concat_obj
    # if there is only one character in concat_obj, that is already seen, it's rule 1
    if nb_elements <= 1:
        return 0

    for i in range(nb_elements):
        # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
        if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + i] \
                != f_oracle.data[actual_char_ind - nb_elements + i]:
            return 0

    # if the actual concat_obj is not the longest common string :
    if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements] == f_oracle.data[actual_char_ind]:
        return 0

    if len(oracles[1]) > level + 1:

        # allocation of structures of level sup
        f_oracle_sup = oracles[1][level + 1][0]
        link_sup = oracles[1][level + 1][1]
        history_next_sup = oracles[1][level + 1][2]
        concat_obj_sup = oracles[1][level + 1][3]

        real_ind = link[f_oracle.sfx[actual_char_ind - nb_elements]]
        real_value = f_oracle_sup.data[real_ind]
        history_k = real_value - 1

        # if concat_obj corresponds to an already known object, return 0.
        if history_next[real_value - 1][1] == concat_obj:
            return 0

        # Structuring.
        # Modification of the structures if they exist :
        # actual level : link, history_next
        # next level : FO, history_next, link, concat_obj
        #
        # there is no need to modify next next level and so because there can not be any structuration between the two
        # nodes that are created in the next level as it's the separation of one new string into two new strings.

        # update of link
        for i in range(f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements, len(link)):
            link[i] = link[i] + 1

        # update of history_next
        j = 0
        nb_node = 0
        letter = ord(history_next[history_k][0])
        history_temp = history_next[history_k]
        history_next.pop(history_k)
        while history_temp[1][j] != concat_obj[0]:
            j += 1
        if j > 0:
            history_element = (chr(letter), history_temp[1][0:j])
            history_next.insert(history_k, history_element)
            letter += 1
            history_k += 1
            nb_node += 1
        history_element = (chr(letter), history_temp[1][j:j + len(concat_obj)])
        history_next.insert(history_k, history_element)
        letter += 1
        history_k += 1
        nb_node += 1
        if j + len(concat_obj) < len(history_temp[1]):
            history_element = (chr(letter), history_temp[1][j + len(concat_obj):])
            history_next.insert(history_k, history_element)
            letter += 1
            history_k += 1
            nb_node += 1
        for i in range(history_k, len(history_next)):
            new_el = (chr(letter), history_next[i][1])
            history_next[i] = new_el
            letter = letter + 1

        # update of the whole FO at next level
        new_fo_sup = oracle_ac.create_oracle('f')
        for i in range(1, real_ind):
            new_state = f_oracle_sup.data[i]
            new_fo_sup.add_state(new_state)
        for i in range(nb_node):
            history_k = f_oracle_sup.data[real_ind] + i
            new_fo_sup.add_state(history_k)
        for i in range(real_ind + 1, len(f_oracle_sup.data)):
            if f_oracle_sup.data[i] < len(history_next) - 1:
                new_state = f_oracle_sup.data[i]
            else:
                new_state = f_oracle_sup.data[i] + nb_node - 1
            new_fo_sup.add_state(new_state)
        oracles[1][level + 1][0] = new_fo_sup

        # TODO : mettre à jour le diagramme formel de niveau sup ici :
        # update of the formal diagram at next level
        formal_diagram_sup = []
        formal_diagram_init(formal_diagram_sup, data_length)
        for i in range(2, len(new_fo_sup.data)):
            actual_char = new_fo_sup.data[i]
            formal_diagram_update(formal_diagram_sup, data_length, actual_char, i)
        oracles[1][level + 1][4] = formal_diagram_sup

        # update of link_sup and history_next_sup if necessary
        print("link : ", link)
        print("history_next: ", history_next)
        print("link_sup : ", link_sup)
        print("history_next_sup : ", history_next_sup)
        print("real_ind : ", real_ind)
        print("real_value : ", real_value)
        if len(link_sup) >= real_ind + 1:
            history_next_sup_value = oracles[1][level + 1][0].data[real_value - 1]
            print("history next sup value : ", history_next_sup_value)
            link_temp = link_sup[real_ind]
            new_letter = history_next_sup[history_next_sup_value][0]
            string = history_next_sup[history_next_sup_value][1]
            for i in range(nb_node - 1):
                link_sup.insert(real_ind + i + 1, link_temp)
                string += chr(new_fo_sup.data[real_ind + i + 1] + letter_diff)
                new_hns = (new_letter, string)
                history_next_sup[history_next_sup_value] = new_hns
            for i in range(history_next_sup_value, len(history_next_sup)):
                new_letter = history_next_sup[i][0]
                old_string = history_next_sup[i][1]
                string = ''
                for k in range(len(old_string)):
                    string += chr(ord(old_string[k]) + nb_node - 1)
                new_hns = (new_letter, string)
                history_next_sup[i] = new_hns
            new_concat_obj_sup = ''

        else:
            new_concat_obj_sup = concat_obj_sup
        print("link_sup : ", link_sup)
        print("history_next_sup : ", history_next_sup)
        # update of concat_obj_sup if needed
        for i in range(len(concat_obj_sup)):
            new_concat_obj_sup += chr(new_fo_sup.data[len(new_fo_sup.data) - len(concat_obj_sup) + i] + letter_diff)
        oracles[1][level + 1][3] = new_concat_obj_sup
    return 1


def rule_4_recomputed_object(oracles, level, actual_char_ind):
    """This function compare the actual concatenated object concat_obj of unstructured characters of the actual level
    with substrings of objects of the upper level stocked in the tab history_next[]. If the strings are similar,
     the previous recognized string is structured and the algorithm rebuild the different FOs and structures back to
     this state and returns 1, otherwise returns 0."""
    # allocation of structures of actual level
    f_oracle = oracles[1][level][0]
    link = oracles[1][level][1]
    history_next = oracles[1][level][2]
    concat_obj = oracles[1][level][3]
    nb_elements = len(concat_obj)

    print("concat obj", concat_obj)
    # Comparisons between concat_obj and the string starting from the suffix of the first char of concat_obj
    # if there is only one character in concat_obj, that is already seen, it's rule 1
    if nb_elements <= 1 or level != 0:
        return 0

    for j in range(nb_elements):
        # if there is a difference between concat_obj and the longest similar suffix of the first char of concat_obj
        if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + j] \
                != f_oracle.data[actual_char_ind - nb_elements + j]:
            return 0

    # if the actual concat_obj is not the longest common string :
    if f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements] == f_oracle.data[actual_char_ind]:
        return 0

    if len(oracles[1]) > level + 1:

        # allocation of structures of level sup
        f_oracle_sup = oracles[1][level + 1][0]

        real_ind = link[f_oracle.sfx[actual_char_ind - nb_elements]]
        real_value = f_oracle_sup.data[real_ind]

        # if concat_obj corresponds to an already known object, return 0.
        if history_next[real_value - 1][1] == concat_obj:
            return 0

    # else, we are in the required conditions and we rebuild the oracles
    # First we go back to the new already-seen state with concat obj as
    level_up = level
    level_tmp = -1
    ind = f_oracle.sfx[actual_char_ind - nb_elements] - 1

    # pour chaque niveau n :
    while len(oracles[1]) > level_up != level_tmp:
        print("NUMBER ORACLE " + str(level_up))
        new_fo = oracle_ac.create_oracle('f')

        # f_oracle
        i = 1
        while i < ind + 1:
            new_state = oracles[1][level_up][0].data[i]
            new_fo.add_state(new_state)
            i += 1

        # link and formal diagram
        if len(oracles[1][level_up][1]) > ind:
            new_ind = oracles[1][level_up][1][ind]
            print("new ind 1", new_ind)
            seg = 0
            oracles[1][level_up][3] = ''
        else:
            new_ind = max(oracles[1][level_up][1])
            print("new ind 2", new_ind)
            seg = 1
        print(oracles[1][level_up][1])
        while i < len(oracles[1][level_up][1]):
            oracles[1][level_up][1].pop(i)
            oracles[1][level_up][4][oracles[1][level_up][0].data[i] - 1][i - 1] = 1
        if level_up != level:
            tmp_concat_obj = ''
            if seg == 0 and len(oracles[1][level_up][1]) > 1:
                while  oracles[1][level_up][1][len(oracles[1][level_up][1]) - 1] == new_ind:
                    tmp_concat_obj = chr(oracles[1][level_up][0].data[len(oracles[1][level_up][1]) - 1] + letter_diff) \
                                     + tmp_concat_obj
                    oracles[1][level_up][1].pop(len(oracles[1][level_up][1]) - 1)

                    # concat_obj
                new_ind = max(oracles[1][level_up][1])
                oracles[1][level_up][3] += tmp_concat_obj

        else:
            # concat_obj
            for j in range(nb_elements):
                element = chr(f_oracle.data[f_oracle.sfx[actual_char_ind - nb_elements] + j] + letter_diff)
                oracles[1][level_up][3] += element
                new_state = oracles[1][level_up][0].data[i + j]
                new_fo.add_state(new_state)

        oracles[1][level_up][0] = new_fo

        print(oracles[1][level_up][0].data)
        print(oracles[1][level_up][1])
        print(oracles[1][level_up][3])
        # next level
        level_tmp = level_up
        if level_up < len(oracles[1]) - 1:
            # history_next
            next_ind = max(oracles[1][level_up + 1][0].data[:new_ind + 1])
            len_max = len(oracles[1][level_up][2])
            for j in range(len_max - next_ind):
                oracles[1][level_up][2].pop(len(oracles[1][level_up][2]) - 1)
            print(oracles[1][level_up][2])

            ind = new_ind
            level_up = level_up + 1

    # Then we go back to the main loop of the structuration function with the correct structure to rebuilt the oracles

    return 1


def rule_5_regathering(concat_obj):
    """ The function returns 1 if the length of the string corresponding to  the concatenated object that are not
    structured in the actual level is higher than one. It returns 0 if the length of the string is equal or less than
    one."""
    if len(concat_obj) > 1:
        return 1
    return 0


# ================================================ SIMILARITY ==========================================================

def char_next_level_similarity(history_next, concat_obj):
    """ The function compare the actual new structured string with structured strings already seen before. For now,
    the strings have to be the exact sames to be considered as similar. The history_next tab is modified according to
    the results and the new string of upper level new_char is returned."""
    for i in range(len(history_next)):
        if len(concat_obj) == len(history_next[i][1]):
            j = 0
            while history_next[i][1][j] == concat_obj[j]:
                j = j + 1
                if j == len(history_next[i][1]):
                    new_char = history_next[i][0]
                    return new_char
    new_char = chr(97 + len(history_next))
    history_next.append((new_char, concat_obj))
    return new_char


# ============================================ AUGMENTED FO ============================================================

def structure_init(flag, level):
    # TODO : faire une version objet
    f_oracle = oracle_ac.create_oracle(flag)
    link = [0]
    history_next = []
    concat_obj = ''
    formal_diagram = []
    formal_diagram_graph = print_formal_diagram_init(level)
    return f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph


# ============================================ FORMAL DIAGRAM ==========================================================

# First implementation computed at the end of the segmentation function
def cognitive_algorithm(data):
    """ This function creates the matrix that represents the formal diagram produce by the adequated string char. It
    returns the matrix corresponding to the formal diagram and the len of the string."""
    len_data = len(data) - 1
    nb_mat = 1
    new_mat = [1 for i in range(len_data)]
    mtx = [new_mat]
    mtx[0][0] = 0
    for i_hop in range(1, len_data):
        j_mat = data[i_hop + 1] - 1
        if j_mat > len(mtx) - 1:
            nb_mat = nb_mat + 1
            new_mat = [1 for i in range(len_data)]
            mtx.append(new_mat)
            mtx[nb_mat - 1][i_hop] = 0
        else:
            mtx[j_mat][i_hop] = 0
    return mtx, len_data


def graph_cognitive_algorithm(char, matrix, data_length):
    """ plot the picture of formal diagram matrix according to its length data_length. The picture is named ofter the
    string char."""
    name = char
    plt.figure(figsize=(12, 6))
    plt.title("Formal diagram of " + name)
    plt.gray()
    plt.imshow(matrix, extent=[0, data_length, len(matrix), 0])
    plt.show()


# Second implementation for an evolutive formal diagram
def print_formal_diagram_init(level):
    print("PRINT formal diagram init")
    fig = plt.figure(figsize=(10, 4))
    plt.title("Formal diagram of level " + str(level))
    plt.xlabel("time in number of states (formal memory)")
    plt.ylabel("material (material memory)")
    plt.gray()
    print("fig.number :", fig.number)
    return fig.number


def print_formal_diagram_update(fig_number, formal_diagram, data_length):
    print("PRINT formal diagram update")
    fig = plt.figure(fig_number)
    string = ""
    for i in range(len(formal_diagram)):
        string += chr(i + letter_diff + 1)
    plt.yticks(range(len(formal_diagram)), string)
    plt.imshow(formal_diagram, extent=[0, data_length, len(formal_diagram), 0])
    plt.pause(0.01)
    return fig.number


def formal_diagram_init(formal_diagram, data_length):
    print("formal diagram init")
    new_mat = [1 for i in range(data_length)]
    formal_diagram.append(new_mat)
    formal_diagram[0][0] = 0
    return 1


def formal_diagram_update(formal_diagram, data_length, actual_char, actual_char_ind):
    print("formal diagram update")
    if actual_char > len(formal_diagram):
        new_mat = [1 for i in range(data_length)]
        formal_diagram.append(new_mat)
        formal_diagram[len(formal_diagram) - 1][actual_char_ind - 1] = 0
    else:
        formal_diagram[actual_char - 1][actual_char_ind - 1] = 0
    return 0


# ============================================ SEGMENTATION FUNCTION ===================================================

def fun_segmentation(oracles, str_obj, data_length, level=0, level_max=-1, end_mk=0):
    """This function browses the string char and structure it at the upper level according to the rules that are applied
    by the extern user. It returns the structured char which is a tab of substring representing upper level object, the
    new string wew_char of upper level with adequated letters and the tab history[] of objects that are seen in this
    level."""

    input_data = [ord(str_obj[i]) - letter_diff for i in range(len(str_obj))]
    if level > oracles[0] and end_mk == 1:
        return 0
    if level > oracles[0]:
        # Initialisation of the structures
        print("[INFO] CREATION OF NEW FO : LEVEL " + str(level) + "...")
        weights = None
        feature = None

        flag = 'f'

        if weights is None:
            weights = {}
            weights.setdefault(feature, 1.0)

        f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph = \
            structure_init(flag, level)
        oracles[1].append([f_oracle, link, history_next, concat_obj, formal_diagram, formal_diagram_graph])

        oracles[0] = level
        level_max = level

    else:
        f_oracle = oracles[1][level][0]
        link = oracles[1][level][1]
        history_next = oracles[1][level][2]
        concat_obj = oracles[1][level][3]
        formal_diagram = oracles[1][level][4]
        formal_diagram_graph = oracles[1][level][5]

    k = len(f_oracle.data) - 1
    # Every new character is analysed.
    i = 0
    while i < len(str_obj):
        print("[INFO] PROCESS IN LEVEL " + str(level))
        f_oracle.add_state(input_data[i])
        actual_char = f_oracle.data[k + i + 1]  # i_th parsed character
        actual_char_ind = k + i + 1
        nb_elements = len(concat_obj)
        print("Actual char processed is " + chr(actual_char + letter_diff))

        # formal diagram is updated with the new char
        if actual_char_ind == 1:
            formal_diagram_init(formal_diagram, data_length)
        else:
            formal_diagram_update(formal_diagram, data_length, actual_char, actual_char_ind)

        oracles[1][level][5] = print_formal_diagram_update(formal_diagram_graph, formal_diagram, data_length)

        # First is the parametrisation of the rules according to the external settings.
        if RULE_1:
            test_1 = rule_1_similarity(f_oracle, actual_char_ind)
        else:
            test_1 = 1
        if RULE_2:
            test_2 = rule_2_not_validated_hypothesis(f_oracle, link, actual_char, actual_char_ind)
        else:
            test_2 = 1
        if not RULE_1 and not RULE_2:
            test_1 = 0
            test_2 = 0
        if RULE_4:
            test_4 = rule_4_recomputed_object(oracles, level, actual_char_ind)
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

        if test_4:
            i = f_oracle.sfx[actual_char_ind - nb_elements] + nb_elements - 1
            actual_char = f_oracle.data[i + 1]
            f_oracle = oracles[1][level][0]
            link = oracles[1][level][1]
            history_next = oracles[1][level][2]
            concat_obj = oracles[1][level][3]
            formal_diagram = oracles[1][level][4]
            formal_diagram_graph = oracles[1][level][5]
            print("input data", actual_char)
            f_oracle.add_state(actual_char)

        # If the tests are positives, there is structuration.
        if ((test_1 and test_2) or test_3 or test_4) and test_5 and \
                (end_mk == 0 or (end_mk == 1 and len(concat_obj) != 0)):
            print("Structuring")

            # Labelling upper level string and updating the different structures
            new_char = char_next_level_similarity(history_next, concat_obj)
            if len(oracles[1]) > level + 1:
                node = len(oracles[1][level + 1][0].data)
            else:
                node = 1
            for ind in range(len(concat_obj)):
                link.append(node)

            # send to the next f_oracle the node corresponding to concat_obj
            fun_segmentation(oracles, new_char, data_length, level + 1, level_max, end_mk)
            print("[INFO] PROCESS IN LEVEL " + str(level))
            concat_obj = ''
        concat_obj = concat_obj + chr(actual_char + letter_diff)
        oracles[1][level][3] = concat_obj

        # Automatically structuring if this is the End Of String
        if level == 0 and i == len(str_obj) - 1:
            end_mk = 1
        if end_mk == 1:
            print("Structuring for the last time at this level...")
            new_char = char_next_level_similarity(history_next, concat_obj)
            if len(oracles[1]) > level + 1:
                node = len(oracles[1][level + 1][0].data)
            else:
                node = 1
            for ind in range(len(concat_obj)):
                link.append(node)
            fun_segmentation(oracles, new_char, data_length, level + 1, level_max, end_mk)
            concat_obj = ''
            oracles[1][level][3] = concat_obj
        i += 1

    return 1


# ===================================================== MAIN ==========================================================

# This is the main loop with all static structures
def main(char_ex):
    # initialisation of the structures
    data_length = len(char_ex)
    level_max = -1
    tab_f_oracle = []
    oracles = [level_max, tab_f_oracle]
    fun_segmentation(oracles, char_ex, data_length)
    new_fd = []

    # printing the results in the shell
    for i in range(len(oracles[1])):
        new_fd.append([chr(tab_f_oracle[i][0].data[j] + letter_diff) for j in range(1, len(tab_f_oracle[i][0].data))])
        print("new_fd_" + str(i) + ": ", new_fd[i])
        print("link_" + str(i) + ": ", oracles[1][i][1])
        print("history next : ", oracles[1][i][2])
    plt.pause(300)


# Here is a simple example with the analysis of a single string 'abacabacdeabfgabachijklmhinopqabacrsrsttu'
def example():
    char_ex2 = 'abacabacdeabfgabachijklmabacdeabhinopqabacrsrsttu'
    char_ex = 'abacabacdeabfgabachijklmhinopqabacrsrsttu'
    main(char_ex)


example()
