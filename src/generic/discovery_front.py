# In this file is computed the discovery front.


def discovery_front_computing(diag, background):
    print("[INFO] Computing the discovery front...")
    """ Compute a tab of the discovery front. Each elements are pairs corresponding to the index of the material and the
    timestamp of appearing."""
    mat = [[0, 0]]
    j = 0
    for i in range(1, len(diag)):
        while diag[i][j][0] == background[0] and diag[i][j][1] == background[1] and diag[i][j][2] == background[2]:
            j = j + 1
        mat.append([j, i])  # couples of (timestamp, nb_material)
    print("[RESULT] Discovery front :")
    print(mat)
    return mat
