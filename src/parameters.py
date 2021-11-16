# ================================================= PARAMETERS =========================================================
# This is the parametrisation file of the system
# Any variable tha can be modified by the users of the system are here.
# In the interface, numbers might be changed by virtual potentiometers, colors...

# ------------- MAIN -----------------
# Main informations about the signal to
# process

NAME = "Geisslerlied"
FORMAT = '.wav'

PATH_OBJ_BASIS = 'cognitive_algorithm_and_its_musical_applications/data/'
PATH_OBJ = PATH_OBJ_BASIS + "Geisslerlied/"
PATH_RESULT = "cognitive_algorithm_and_its_musical_applications/results/The_Wknd/"

teta = 0.975  # 0.976
if teta > 1:
    teta = 1
elif teta < 0:
    teta = 0

superpose_threshold = 0.94
if superpose_threshold > 1:
    superpose_threshold = 1
elif superpose_threshold < 0:
    superpose_threshold = 0

min_matrix = 0.94
if min_matrix > 1:
    min_matrix = 1
elif min_matrix < 0:
    min_matrix = 0

d_threshold = 0.1  # 0.1 for dynamic, 150 for fourier
if d_threshold < 0:
    d_threshold = 0
# processing must be str 'symbols' or 'signal'
processing = 'signal'
verbose = 0


# === SIMILARITY AND SEGMENTATION RULES ===
# -------- SIGNAL SIMILARITY RULES --------
DIFF_CONCORDANCE = 1
EUCLID_DISTANCE = 0

if DIFF_CONCORDANCE + EUCLID_DISTANCE != 1:
    DIFF_CONCORDANCE = 1
    EUCLID_DISTANCE = 0

# ------ SIGNAL SEGMENTATION RULES --------
DIFF_FOURIER = 0
DIFF_DYNAMIC = 1

if DIFF_FOURIER + DIFF_DYNAMIC != 1:
    DIFF_FOURIER = 1
    DIFF_DYNAMIC = 0

# ------- SYMBOLS SIMILARITY RULES --------
STRICT_EQUALITY = 0
ALIGNMENT = 1

if STRICT_EQUALITY + ALIGNMENT != 1:
    STRICT_EQUALITY = 0
    ALIGNMENT = 1

# -------SYMBOLS SEGMENTATION RULES -------
# Rules that are activated or not and their
# parameters

RULE_1 = 1
RULE_2 = 1
RULE_3 = 1
RULE_4 = 0
RULE_5 = 1

ALIGNEMENT_rule3 = 0
ALIGNEMENT_rule4 = 0

# ------------- ALIGNEMENT ----------------
# Alignement parameters to reajust similarity
# matrix values and to define the compared
# symbols

QUOTIENT = 100
TRANSPOSITION = 1
LETTER_DIFF = 96

GAP_VALUE = -5
EXT_GAP_VALUE = -1
GAP = chr(0)
CORREC_VALUE = GAP_VALUE/2

# -------- SIGNAL SIM FUNCTIONS -----------
# parameters for signal similarity computation

# fft : 0.91; mfcc : 0.019 pour 50; cqt : 0.97
# at precision 2, 0.927 at precision 1
TETA = teta
AUDIBLE_THRESHOLD = 0.00001
# fft : 35; mfcc : 60 # cqt : 140
D_THRESHOLD = d_threshold
GRAPH_COMPARISON = 0

# ----------- DATA PROCESSING --------------
# parameters for data processing

SR = 22050
HOP_LENGTH = 1024

PRECISION = 4
NB_NOTES = 48*PRECISION
NB_MFCC = 50
INIT = 0

MFCC_BIT = 0
CQT_BIT = 1
FFT_BIT = 0

if MFCC_BIT + CQT_BIT + FFT_BIT != 1:
    MFCC_BIT = 0
    CQT_BIT = 1
    FFT_BIT = 0

if CQT_BIT:
    NB_VALUES = NB_NOTES
elif MFCC_BIT:
    NB_VALUES = NB_MFCC
else:
    NB_VALUES = 0

# cqt
NOTES_PER_OCTAVE = 12*PRECISION
NOTE_MIN = 'C3'

# fft
# 0.5 for quarter_tone, 1 for
# half-tone, 2 for tone
TONE_PRECISION = 0.125
DIV = 20

TIME_STATS = 0
MFCC_NORMALISATION = 0
CLEAN_SPECTRUM = 0

# ------------- MIDI ------------------
# parameters for obtention of formal
# diagram from MIDI file

TEMPO = 120

# ------------ DISPLAY ----------------

# note : matrices are created in HSV
# H between 0 and 179
# S between 0 and 255
# V between 0 and 255

BASIC_FRAME = (0, 0, 0)  # black
BACKGROUND = (0, 0, 255)  # white
SEGMENTATION = (0, 255, 255)  # red
SEG_ERROR = (60, 255, 255)  # light green
CLASS_ERROR = (60, 255, 150)  # dark green
SILENT_FRAME = BACKGROUND



# --------- INTERFACE ---------------
# parameters to save or to show in .bmp
# or from pyplot
TO_SAVE_BMP = 0
TO_SHOW_BMP = 0
TO_SAVE_PYP = 0
TO_SHOW_PYP = 1

# to show or not the oracle at level 0
PLOT_ORACLE = 0
# to show the evolution of the formal
# diagrams
EVOL_PRINT = 1

# ------------ ALGOCOG ----------------

CORRECTION_BIT = 0
CORRECTION_BIT_COLOR = 0
SEGMENTATION_BIT = 0
WRITE_RESULTS = 0

NB_SILENCE = 1024*16

ALGO_VMO = 1
ALGO_REP = 0
ALGO_USUAL = 0

# ------------ VMO ---------------

PARCOURS = 1
INCERTITUDE = 3
SUFFIX_METHOD = 'complete'  # 'inc' ou 'complete'

SYNTHESIS = 0
