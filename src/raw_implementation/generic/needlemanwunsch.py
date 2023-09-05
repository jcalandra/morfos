#!/usr/bin/env python
"""
initial code imported from slowkow/needlemanwunsch.py
modification added  by Joséphine Calandra to adapt alignment for musical sequences

The Needleman-Wunsch Algorithm
==============================
This is a dynamic programming algorithm for finding the optimal alignment of
two strings.

LICENSE
This is free and unencumbered software released into the public domain.
Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.
In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
For more information, please refer to <http://unlicense.org/>
"""
import sys
import numpy as np
import parameters

from Bio import pairwise2
from Bio.Align import substitution_matrices

gap_value = parameters.GAP_VALUE
extend_gap_value = parameters.EXT_GAP_VALUE
gap = parameters.GAP
correc_value = parameters.CORREC_VALUE

def nw(x, y, matrix=None, match_value = 1, mismatch_value = 0, gap_value = 0.5, extended_gap_value = -1, gap = "-"):
    nx = len(x)
    ny = len(y)
    # Optimal score at each possible pair of characters.
    F = np.zeros((nx + 1, ny + 1))
    F[1][0] = gap_value
    F[0][1] = gap_value
    for i in range(1, nx + 1):
        F[i][0] = (i - 1) * extended_gap_value + gap_value
    for i in range(1, ny + 1):
        F[0][i] = (i - 1) * extended_gap_value + gap_value

    # Pointers to trace through an optimal aligment.
    P = np.zeros((nx + 1, ny + 1))
    P[:,0] = 3
    P[0,:] = 4
    # Temporary scores.
    t = np.zeros(3)
    for i in range(nx):
        for j in range(ny):
            if matrix == None:
                if x[i] == y[j]:
                    t[0] = F[i,j] + match_value
                else:
                    t[0] = F[i,j] + mismatch_value
            else:
                t[0] = F[i,j] + find_matrix_autosim(x[i], y[j], matrix)
            if P[i,j+1] in [3, 4, 7, 5, 6, 9]:
                t[1] = F[i,j+1] + extended_gap_value
            else:
                t[1] = F[i,j+1] + gap_value
            if P[i+1,j] in [3, 4, 7, 5, 6, 9]:
                t[2] = F[i+1,j] + extended_gap_value
            else:
                t[2] = F[i+1,j] + gap_value
            tmax = np.max(t)
            F[i+1,j+1] = tmax
            if t[0] == tmax:
                P[i+1,j+1] += 2
            if t[1] == tmax:
                P[i+1,j+1] += 3
            if t[2] == tmax:
                P[i+1,j+1] += 4
    # Trace through an optimal alignment.
    i = nx
    j = ny
    rx = []
    ry = []
    while i > 0 or j > 0:
        if P[i,j] in [2, 5, 6, 9]:
            rx.append(x[i-1])
            ry.append(y[j-1])
            i -= 1
            j -= 1
        elif P[i,j] in [3, 5, 7, 9]:
            rx.append(x[i-1])
            ry.append(gap)
            i -= 1
        elif P[i,j] in [4, 6, 7, 9]:
            rx.append(gap)
            ry.append(y[j-1])
            j -= 1
    # Reverse the strings.
    rx = ''.join(rx)[::-1]
    ry = ''.join(ry)[::-1]
    return ['\n'.join([rx, ry]), tmax]

def find_matrix_autosim(char1, char2, matrix):
    str = matrix[0]
    autosim = matrix[1]
    c1 = None
    c2 = None
    for i in range(len(str)):
        if char1 == str[i]:
            c1 = i
        if char2 == str[i]:
            c2 = i
        if c1 != None and c2 != None:
            return autosim[c1][c2]
    sys.exit("The letter you looking for in the autosimilarity tab does not exist")

def compute_distance(rx, ry, matrix, match_value, mismatch_value, gap_value, gap):
    distance = 0
    assert(len(rx) == len(ry))
    for i in range(len(rx)):
        if rx[i] == gap or ry[i] == gap:
            distance += gap_value
        else:
            if matrix == None:
                if rx[i] == ry[i]:
                    distance += match_value
                else:
                    distance += mismatch_value
            else:
                distance += find_matrix_autosim(rx[i], ry[i], matrix)
    return distance


def tests():
    x = "GATTACA"
    y = "GACCTTACA"
    M = [[1, 0.8, 0.4, 0.9, 0], [0.8, 1, 0.7, 0.85, 0.56], [0.4, 0.7, 1, 0.2, 0.87], [0.9, 0.85, 0.2, 1, 0.5], [0, 0.56, 0.87, 0.5, 1]]
    M2 = [[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]]
    matrix = ["GATCU", M]
    print(nw(x, y, matrix, gap_value = -1, extended_gap_value=-0.5, gap=gap))

    np_mat = np.array(matrix[1])
    matrix = substitution_matrices.Array(alphabet=matrix[0], dims=2, data=np_mat)
    nw_align =pairwise2.align.globalds(x, y, matrix, -1, -0.5, gap_char=gap)
    print(nw_align)
    print(nw_align[0][2])