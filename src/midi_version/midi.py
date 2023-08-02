import music21
import matplotlib.pyplot as plt
import parameters as prm
import numpy as np
import cv2
import os

# This file contains an implementation of formal diagram computation from a MIDI file (non-hierarchical implementation)

SR = prm.SR
HOP_LENGTH = prm.HOP_LENGTH
TEMPO = prm.TEMPO

BACKGROUND = prm.BACKGROUND
BASIC_FRAME = prm.BASIC_FRAME

NB_SILENCE = prm.NB_SILENCE

AUDIBLE_THRESHOLD = prm.AUDIBLE_THRESHOLD

PATH_RESULT = "../../results/"


# TODO : mettre ce code dans le dossier src et modifier les tests en conséquence
# TODO : changer les matrices en numpy array
# TODO : modifier l'affichage en fonction du type de matrice obtenu
# TODO : enregistrer une image bmp juste du diagramme
# TODO : ne pas diviser à la sous-frame, garder la note comme niveau de matériau


# =================================================== DATA COMPUTING ===================================================
def open_midi(midi_path):
    """ Open and read MIDI file at MIDI path."""
    mf = music21.midi.MidiFile()
    mf.open(midi_path)
    mf.read()
    mf.close()
    return music21.midi.translate.midiFileToStream(mf)


def extract_notes(midi_part):
    """ Extract the notes and volumes from a MIDI file."""
    print("[INFO] Extracting notes of the MIDI file...")
    parent_element = []
    ret = []
    vol = []
    for nt in midi_part.flat.notes:
        if isinstance(nt, music21.note.Note):
            ret.append(max(0.0, nt.pitch.ps))
            parent_element.append(nt)
            vol.append(nt.volume.velocity)
        elif isinstance(nt, music21.chord.Chord):
            for pitch in nt.pitches:
                ret.append(max(0.0, pitch.ps))
                parent_element.append(nt)
                vol.append(nt.volume.velocity)
    return ret, vol, parent_element


# ============================================== SIMILARITY ============================================================
def comparison(i_hop, ret, vol, mat):
    """ Return the corresponding materials of the notes contained in the list 'ret'."""
    if vol[i_hop] < AUDIBLE_THRESHOLD:
        return 0
    for j_hop in range(i_hop):
        if ret[i_hop] == ret[j_hop] and mat[j_hop + 1] != 0:
            return mat[j_hop + 1]
    return -1


# ============================================ FORMAL DIAGRAM ==========================================================
def algo_cog(ret, vol, time):
    print("[INFO] Computing the cognitive algorithm of the MIDI extract...")
    """ Compute the formal diagram according to the list of notes 'ret'."""
    # initialise matrix of each hop coordinates
    nb_hop_sec = SR / HOP_LENGTH
    sil_hop = int(NB_SILENCE/HOP_LENGTH)
    n = (time[-1] - time[-2])  # n corresponds to the length of the last note (in sec) # il faut trouver mieux pour
    # avoir le tempo
    # n = (time[-3] - time[-4])
    midi_length = int((time[-1] + n) * nb_hop_sec + sil_hop + 1)
    nb_note = len(ret)
    print("[RESULT] midi length = ", midi_length)
    mat = [0]  # matrix where each accessor correspond to state and each result is the adequate material
    nb_mat = 1  # number of materials

    new_mat = np.ones((1, midi_length, 3), np.uint8)
    for i in range(midi_length):
        new_mat[0][i] = BACKGROUND  # new line printed for a new material
    mtx = new_mat.copy()  # The matrix is initialized with the first material which is silence material

    new_mat = np.ones((1, midi_length, 3), np.uint8)
    for i in range(midi_length):
        new_mat[0][i] = BACKGROUND
    mtx = np.concatenate((mtx, new_mat))
    nb_mat = nb_mat + 1
    mat.append(nb_mat - 1)

    value = 255 - vol[0] * 255
    color = (BASIC_FRAME[0], BASIC_FRAME[1], value)
    k = sil_hop
    while k < sil_hop + round(time[1] * nb_hop_sec):
        mtx[1][k] = color
        k = k + 1

    for i_hop in range(1, nb_note):
        j_mat = comparison(i_hop, ret, vol, mat)
        value = 255 - vol[i_hop] * 255
        color = (BASIC_FRAME[0], BASIC_FRAME[1], value)
        if j_mat == -1:
            nb_mat = nb_mat + 1
            mat.append(nb_mat - 1)
            new_mat = np.ones((1, midi_length, 3), np.uint8)
            for i in range(midi_length):
                new_mat[0][i] = BACKGROUND
            mtx = np.concatenate((mtx, new_mat))
            j_mat = nb_mat - 1

        else:
            mat.append(j_mat)

        while i_hop < nb_note - 1 and k < sil_hop + (time[i_hop + 1] * nb_hop_sec):
            mtx[j_mat][k] = color
            k = k + 1
        while i_hop == nb_note - 1 and k < midi_length:
            mtx[j_mat][k] = color
            k = k + 1

    mtx = cv2.cvtColor(mtx, cv2.COLOR_HSV2BGR)

    return mtx


# ============================================== MAIN FUNCTION =========================================================
def interface(midi_path, tempo):
    """Compute and display the formal diagrams obtained from the MIDI file at 'midi_path'."""
    midi = open_midi(midi_path)
    ratio = tempo / 60
    top = midi.parts[0].flat.notes
    freq, vol, parent_element = extract_notes(top)
    time = [n.offset / ratio for n in parent_element]
    print("[RESULT] notes = ", freq)
    print("[RESULT] time = ", time)

    matrix = algo_cog(freq, vol, time)

    plt.figure(figsize=(32, 20))
    name_form = midi_path.split('/')[-1]
    name = name_form.split('.')[0]
    file_name = "diagcog" + name + "-midi_" + str(HOP_LENGTH) + ".png"
    plt.title("Diagramme formel de " + name + " hoplength" + str(HOP_LENGTH))
    plt.gray()
    plt.xlabel("temps (mémoire forme)")
    plt.ylabel("matériau (mémoire matériau)")
    plt.imshow(matrix, extent=[0, (time[-1] + 1), len(matrix), 0])
    path_results = PATH_RESULT + name + "/test_diff/"
    plt.savefig(path_results + file_name.split('.')[0])
    plt.show()
    plt.close()
    return matrix


# ================================================= EXAMPLE ============================================================
def example_Geisslerlied():
    """ Main function with Geisslerlied as an example."""
    name = "reflets_dans_leau"
    tempo = TEMPO
    path = os. getcwd()
    print("Le répertoire courant est : " + path)
    midi_path = 'cognitive_algorithm_and_its_musical_applications/data/MIDI/' + name + '.mid'
    interface(midi_path, tempo)


example_Geisslerlied()
