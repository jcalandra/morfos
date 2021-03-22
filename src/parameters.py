# TODO : faire un fichier de vérification de validation des paramètres.
# TODO : faire en sorte d'afficher tous les paramètres dans un fichier externe lors de lancement de tests

# ------------- MAIN -----------------

NAME = "MozartK545_rondo"
FORMAT = '.wav'

PATH_OBJ_BASIS = 'cognitive_algorithm_and_its_musical_applications/data/'
PATH_OBJ = PATH_OBJ_BASIS + 'Mozart/'
PATH_RESULT = "cognitive_algorithm_and_its_musical_applications/results/Mozart/"

SR = 22050
HOP_LENGTH = 1024  # cqt : 512

LETTER_DIFF = 1

PRECISION = 4
NB_NOTES = 48*PRECISION
NB_MFCC = 50
TETA = 0.976  # fft : 0.91; mfcc : 0.019 pour 50; cqt : 0.903 à précision 2, 0.927 à précision 1
INIT = 0
QUOTIENT = 100

ALGO_VMO = 1
ALGO_REP = 0
ALGO_USUAL = 0

SUFFIX_METHOD = 'complete'  # 'inc' ou 'complete'

# ------------ SIM FUNCTIONS --------------

MFCC_BIT = 0
CQT_BIT = 1
FFT_BIT = 0

AUDIBLE_THRESHOLD = 0.00001
D_THRESHOLD = 140  # fft : 25; mfcc : 60 # cqt : 140
GRAPH_COMPARISON = 0

if CQT_BIT:
    NB_VALUES = NB_NOTES
elif MFCC_BIT:
    NB_VALUES = NB_MFCC
else:
    NB_VALUES = 0

# --------- INTERFACE ---------------

TO_SAVE_BMP = 0
TO_SHOW_BMP = 0
TO_SAVE_PYP = 0
TO_SHOW_PYP = 1

# ------- DATA COMPUTING ------------

# cqt
NOTES_PER_OCTAVE = 12*PRECISION
NOTE_MIN = 'C3'

# fft
TONE_PRECISION = 0.125  # 0.5 for quarter_tone, 1 for half-tone, 2 for tone
DIV = 20

# ------------- MIDI ------------------

TEMPO = 120

# ------------ ALGOCOG ----------------

# note : matrices are created in HSV
# H between 0 and 179
# S between 0 and 255
# V between 0 and 255

BASIC_FRAME = (0, 0, 0)  # black
BACKGROUND = (0, 0, 255)  # white
SEGMENTATION = (0, 255, 255)  # red
SEG_ERROR = (60, 255, 255)  # light green
CLASS_ERROR = (60, 255, 150)  # dark green

CORRECTION_BIT = 1
CORRECTION_BIT_COLOR = 0
SEGMENTATION_BIT = 0
WRITE_RESULTS = 0

NB_SILENCE = 1024*16

# ------------ VMO ---------------

REPRESENTANTS = 1
PARCOURS = 1
INCERTITUDE = 3


def test():
    if (ALGO_VMO + ALGO_REP + ALGO_USUAL) != 1:
        print("ERROR : you must choose one type of algorithm: ALGO_VMO, ALGO_REP or ALGO_USUAL")
    if (MFCC_BIT + CQT_BIT + FFT_BIT) != 1:
        print("ERROR : you must choose one type of analysis: MFCC, CQT or FFT")
    if SUFFIX_METHOD != ('complete' or 'inc'):
        print("WARNING : suffix method might be 'complete' or 'inc' ")
