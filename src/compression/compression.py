# This file is not useful to compute the formal diagrams
# It contains the implementation of a encoding function in order to obtain a
# encoded char from formal diagrams.

# 'nb_materials' is a list that corresponds to the number of material already encoded for each formal diagram.
# 'encoded_char' corresponds to the final encoded char
# 'dictionary' is a dictionary that list for each level the couples that corresponds to an actual-level material and the
# corresponding constituent materials of lower level
# 'formal_diagrams are the final decoded formal diagrams.
global nb_materials
global encoded_char
global dictionary
global formal_diagrams


def convert(fd_str, lvl, mso, t_start, t_end):
    """ Takes as entry the multi-scale oracle data structure 'classes_mso' and a level 'lvl' and time boundaries 't_start' and
    't_end'. Returns a character string corresponding to the adequate sub formal diagram. """
    oracle = mso[lvl][0]
    for i in range(t_start, t_end):
        fd_str.append(oracle.data[i] - 1)
    return fd_str


def parse(fd_str):
    """ Takes as entry the character strings corresponding to the materials of the formal diagram at a specific level
    'lvl_str'. Return the first character of this string and modify it by deleting this first character. """
    if len(fd_str) == 0:
        return None, fd_str
    else:
        c = fd_str[0]
        fd_str = fd_str[1:]  # copy the reference, use numpy references if you want to work with views on references
    return c, fd_str


def already_seen(lvl, m_object):
    """ Takes 'object' as imput and return 0 if this object has already been seen in this level. Otherwise returns 1."""
    global nb_materials
    if m_object > nb_materials[lvl]:
        nb_materials[lvl] = m_object
        return 0
    return 1


def get_boundaries(lvl, mso, t_start):
    """ Return the lower-level boundaries corresponding to the character at stat 't_start' and level 'lvl'."""
    link = mso[lvl - 1][1]
    link_r = link.copy()
    link_r.reverse()
    k_init = link.index(t_start)
    k_end = len(link) - link_r.index(t_start)
    return k_init, k_end


def write(char_object):
    """ Add 'char_object' to the end of the compressed char 'encoded_char'."""
    global encoded_char
    encoded_char.append(char_object)
    return 0


def add_dict(level, char):
    """ Add new materials labeled 'char' in the adequate level 'level' and in the corresponding couple of upper
    level. """
    global dictionary
    if char == '(' or (level == 0 and len(dictionary[0]) < char + 1):
        char = len(dictionary[level])
        dictionary[level].append([char, []])
    if level < len(dictionary) - 1:
        dictionary[level + 1][len(dictionary[level + 1]) - 1][1].append(char)
    return char


def add_df(level, char):
    """ Write a new material labeled 'char' in the formal diagram of level 'level'."""
    global formal_diagrams
    if char is not None:
        formal_diagrams[level].append(char)
    return 0


def add_recursive_df(level, char):
    """ Write a material 'char' in the formal diagram of level 'level' and all the adequate material in the lower
    levels"""
    global formal_diagrams
    char = min(char, len(dictionary[level]) - 1)
    add_df(level, char)
    if level > 0:
        for i in range(len(dictionary[level][char][1])):
            add_recursive_df(level - 1, dictionary[level][char][1][i])
        level -= 1
    return 0


def encode(lvl, mso, fd_str, t_start=1, t_end=1):
    fd_str = convert(fd_str, lvl, mso, t_start, t_end)
    c, fd_str = parse(fd_str)
    while c is not None:
        if already_seen(lvl, c) or lvl == 0:
            t_start += 1
            write(c)
            c, fd_str = parse(fd_str)
        else:
            write('(')
            t_start_inf, t_end_inf = get_boundaries(lvl, mso, t_start)
            encode(lvl - 1, mso, fd_str=[], t_start=t_start_inf, t_end=t_end_inf)
            c, fd_str = parse(fd_str)
            t_start += 1
            write(')')


def decode(level):
    global encoded_char
    char, encoded_char = parse(encoded_char)
    while char != ')':
        if len(encoded_char) == 0:
            new_char = add_dict(level, char)
            add_df(level, new_char)
            break
        if char == '(':
            new_char = add_dict(level, char)
            add_df(level, new_char)
            decode(level - 1)
        else:
            add_dict(level, char)
            add_recursive_df(level, char)
        char, encoded_char = parse(encoded_char)
    parse(encoded_char)