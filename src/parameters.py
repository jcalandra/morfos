# ================================================= PARAMETERS =========================================================
# This is the parametrisation file of the system
# Any variable tha can be modified by the users of the system are here.
# In the interface, numbers might be changed by virtual potentiometers, colors...

# ------------- MAIN -----------------
# Main informations about the signal to process

NAME = "Geisslerlied"
FORMAT = '.wav'

PATH_OBJ_BASIS = 'cognitive_algorithm_and_its_musical_applications/data/'
PATH_OBJ = PATH_OBJ_BASIS + "Geisslerlied/"
PATH_RESULT = "cognitive_algorithm_and_its_musical_applications/results/"

global lambda_0, gamma, alpha, delta, beta
global lambda_tab, gamma_tab, alpha_tab, delta_tab, beta_tab
global lambda_time, gamma_time, alpha_time, delta_time, beta_time
global total_cost, total_cost_tab, total_cost_sum, total_cost_time

# This is the similarity threshold
teta = 0.975
if teta > 1:
    teta = 1
elif teta < 0:
    teta = 0

# This is the segmentation threshold
d_threshold = 150  # exemple of values: 0.1 for dynamic, 150 for fourier
if d_threshold < 0:
    d_threshold = 0

# This is a boolean parameter to display or not a pseudo-polyphony. Work only with MSO implementation.
POLYPHONY = 0

# A value that determine the color variation if pseudo-polyphony is displayed
min_matrix = 0.999
if min_matrix >= 1:
    min_matrix = 0.999
elif min_matrix < 0:
    min_matrix = 0

# Choose here either to process the cognitive algorithm from signal or character string
# processing must be str 'symbols' or 'signal'
processing = 'signal'

# Display comments
verbose = 0

# === SIMILARITY AND SEGMENTATION RULES ===
# -------- SIGNAL SIMILARITY RULES --------
DIFF_CONCORDANCE = 1
EUCLID_DISTANCE = 0

if DIFF_CONCORDANCE + EUCLID_DISTANCE != 1:
    DIFF_CONCORDANCE = 1
    EUCLID_DISTANCE = 0

# ------ SIGNAL SEGMENTATION RULES --------
DIFF_FOURIER = 1
DIFF_DYNAMIC = 0

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
# Definitions in segmentation_rules_mso.py

RULE_1 = 1
RULE_2 = 1
RULE_3 = 1
RULE_4 = 0
RULE_5 = 1

ALIGNEMENT_rule3 = 0
ALIGNEMENT_rule4 = 0

# ============ SIMILARITY AND SEGMENTATION
# SPECIFIC PARAMETRISATION ===============
# ------------- ALIGNEMENT ----------------
# Alignement parameters
# quotient to divide then multiply the
# alignment value for precision
QUOTIENT = 100
#useless parameter for now
TRANSPOSITION = 1

# letter to numbers difference
# for symbols put letter_diff = 96
# for signal put letter_diff = 0
LETTER_DIFF = 96

# Reajust the similarity matrix values
GAP_VALUE = -5
EXT_GAP_VALUE = -1
CORREC_VALUE = GAP_VALUE/2
# chosen Gap character
GAP = chr(0)

# -------- SIGNAL SIM FUNCTIONS -----------
# parameters for signal similarity computation

#Value exemples for similarity threshold:
# fft : 0.91; mfcc : 0.019 pour 50; cqt : 0.97
# at precision 2, 0.927 at precision 1
TETA = teta

# Value under with the signal is considered as silence
AUDIBLE_THRESHOLD = 0.00001

# value exemples for segmentation threshold:
# fft : 35; mfcc : 60 # cqt : 140
D_THRESHOLD = d_threshold

# Display similarity values and similarity threshold. outdated
GRAPH_COMPARISON = 0

# ========== DATA PROCESSING ===========
# parameters for data processing

SR = 22050
HOP_LENGTH = 1024
if processing == 'symbols':
    SR = 1
    HOP_LENGTH = 1

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

# ------------ ALGOCOG ----------------
# At signal level only

# Boolean to chose to reclassify or not
# transitory frames
CORRECTION_BIT = 1
# Boolean to chose to print in different
# color or not transitory frames that
# are moves
CORRECTION_BIT_COLOR = 0
# Boolean to chose to print in different
# color or not segmentation frames
SEGMENTATION_BIT = 0
# Boolean to chose to write some statistics
# in a text file
WRITE_RESULTS = 0

# Number of frames corresponding to silence
# that we want to add at the beggining of the
# audio file
NB_SILENCE = 1024*16

# Type of algorithm we want to use. ALGO_REP
# and ALGO_USUAL ar outdated.
ALGO_VMO = 1
ALGO_REP = 0
ALGO_USUAL = 0


# ------------ DISPLAY ----------------
# Only for level 0
# For the upper levels, background is white
# by default and each objects color alternate
# between four different greys

# note : matrices are created in HSV
# H between 0 and 179
# S between 0 and 255
# V between 0 and 255

BASIC_FRAME = (0, 0, 0)  # black
BACKGROUND = (0, 0, 255)  # white
SEGMENTATION = (0, 255, 255)  # red

# when CORRECTION BIT is activated and a
# frame is moved because of wrong segmentation
# (SEG_ERROR) or similarity (CLASS ERROR)
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

# to show or not the oracles
PLOT_ORACLE = 0
# to show the evolution of the formal
# diagrams
EVOL_PRINT = 0

# ------------ VMO ---------------
# Parameters that are specifics to the
# VMO

# activate for more flexibility in the
# choice of the materials
PARCOURS = 1
# If parcours is activate, choose how much
# frames can be modified backward
INCERTITUDE = 3

# Type of VMO we want to use. Ref to the
# VMO documentation for more information
SUFFIX_METHOD = 'complete'  # 'inc' ou 'complete'

# If we want to resynthesis the obtained VMO
# at level 0.
SYNTHESIS = 0

# COSTS
# TODO: le calcul des coûts n'est pas encore finalisé.
COMPUTE_COSTS = 1
cost_new_oracle = 1

cost_numerisation = 1
cost_desc_computation = 1
cost_oracle_acq_signal = 1
cost_seg_test_1 = 1

cost_new_mat_creation = 1
cost_maj_historique = 1
cost_maj_df = 1
cost_oracle_acq_symb = 1
cost_seg_test_2 = 1
cost_maj_concat_obj = 1
cost_test_EOS = 1

cost_comparaison_2 = 1
cost_labelisation = 1
cost_maj_link = 1
cost_level_up = 1