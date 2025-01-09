# ================================================= PARAMETERS =========================================================
# This is the parametrisation file of the system
# Any variable tha can be modified by the users of the system are here.
# In the interface, numbers might be changed by virtual potentiometers, colors...

import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
project_root = str(file.parents[1])

import json
with open(project_root + '/../parameters.json') as json_parameters:
   data=json.load(json_parameters)

# ------------- MAIN -----------------
# Main informations about the signal to process

NAME = data["NAME"]
FORMAT = data["FORMAT"]

PATH_SOUND = project_root + data["PATH_SOUND"]
PATH_RESULT = project_root + data["PATH_RESULT"]

# This is the similarity threshold
teta = data["teta"]
if teta > 1:
   teta = 1
elif teta < 0:
   teta = 0

# This is the segmentation threshold
d_threshold = data["d_threshold"]  # exemple of values: 0.1 for dynamic, 150 for fourier
if d_threshold < 0:
   d_threshold = 0

# This is a boolean parameter to display or not a pseudo-polyphony. Work only with MSO implementation.
lvl0notcompute = data["lvl0notcompute"]
POLYPHONY = data["POLYPHONY"]

# A value that determine the color variation if pseudo-polyphony is displayed
min_matrix = data["min_matrix"]
if min_matrix >= 1:
   min_matrix = 0.999
elif min_matrix < 0:
   min_matrix = 0

# Choose here either to process the cognitive algorithm from signal or character string
# processing must be str 'symbols' or 'signal' or 'vectors'
if FORMAT == ".wav" or FORMAT == ".mp3":
   processing = "signal"
elif FORMAT == ".npy":
   processing = "vectors"
else:
   processing = "symbols"
to_transpose = data["to_transpose"]
is_micro = data["is_micro"]

# === SIMILARITY AND SEGMENTATION RULES ===
# -------- SIGNAL SIMILARITY RULES --------
DIFF_CONCORDANCE = data["DIFF_CONCORDANCE"]
EUCLID_DISTANCE = data["EUCLID_DISTANCE"]

if DIFF_CONCORDANCE + EUCLID_DISTANCE != 1:
   DIFF_CONCORDANCE = 1
   EUCLID_DISTANCE = 0

# ------ SIGNAL SEGMENTATION RULES --------
DIFF_FOURIER = data["DIFF_FOURIER"]
DIFF_DYNAMIC = data["DIFF_DYNAMIC"]

if DIFF_FOURIER + DIFF_DYNAMIC != 1:
   DIFF_FOURIER = 1
   DIFF_DYNAMIC = 0

# ------- SYMBOLS SIMILARITY RULES --------
STRICT_EQUALITY = data["STRICT_EQUALITY"]
ALIGNMENT = data["ALIGNMENT"]

if STRICT_EQUALITY + ALIGNMENT != 1:
   STRICT_EQUALITY = 0
   ALIGNMENT = 1

# -------SYMBOLS SEGMENTATION RULES -------
# Rules that are activated or not and their
# parameters
# Definitions in segmentation_rules_mso.py

RULE_1 = data["RULE_1"]
RULE_2 = data["RULE_2"]
RULE_3 = data["RULE_3"]
RULE_4 = data["RULE_4"]
RULE_5 = data["RULE_5"]
RULE_5b = data["RULE_5b"]
RULE_6 = data["RULE_6"]
RULE_7 = data["RULE_7"]
RULE_8 = data["RULE_8"]
RULE_9 = data["RULE_9"]
SYMB_MRULES = [RULE_1, RULE_2, RULE_3, 0, 0, RULE_6, RULE_7, RULE_8, RULE_9]
SYMB_PRULES = [0, 0, 0, RULE_4, RULE_5, RULE_6, RULE_7, RULE_8, 0]

RULE1_DISSIMILARITY = data["RULE1_DISSIMILARITY"]
RULE2_ISOLATION = data["RULE2_ISOLATION"]
RULE3_REPETITION = data["RULE3_REPETITION"]
SIG_MRULES = [RULE1_DISSIMILARITY, 0, RULE3_REPETITION]
SIG_PRULES = [0, RULE2_ISOLATION, RULE3_REPETITION]
#RULES = [SYMB_MRULES, SYMB_PRULES]

ALIGNEMENT_rule3 = data["ALIGNEMENT_rule3"]
ALIGNEMENT_rule4 = data["ALIGNEMENT_rule4"]
lower_bound_rule6 = data["lower_bound_rule6"]
higher_bound_rule6 = data["higher_bound_rule6"]

compute_level0 = data["compute_level0"]

# ============ SIMILARITY AND SEGMENTATION
# SPECIFIC PARAMETRISATION ===============
# ------------- ALIGNEMENT ----------------
# Alignement parameters
# quotient to divide then multiply the
# alignment value for precision
QUOTIENT = data["QUOTIENT"]
#useless parameter for now
TRANSPOSITION = data["TRANSPOSITION"]

# letter to numbers difference
# for symbols put letter_diff = 96
# for signal put letter_diff = 0
# to avoid bugs with alignment method, put letter_diff = 127
LETTER_DIFF = data["LETTER_DIFF"]

# Reajust the similarity matrix values
GAP_VALUE = data["GAP_VALUE"] #-5
EXT_GAP_VALUE = data["EXT_GAP_VALUE"] #-1
CORREC_VALUE = GAP_VALUE/2
# chosen Gap character
GAP = chr(data["GAP"])

# -------- SIGNAL SIM FUNCTIONS -----------
# parameters for signal similarity computation

#Value exemples for similarity threshold:
# fft : 0.91; mfcc : 0.019 pour 50; cqt : 0.97
# at precision 2, 0.927 at precision 1
TETA = teta

# Value under with the signal is considered as silence
AUDIBLE_THRESHOLD = data["AUDIBLE_THRESHOLD"]

# value exemples for segmentation threshold:
# fft : 35; mfcc : 60 # cqt : 140
D_THRESHOLD = d_threshold

# maximum number of material per level that are allowed:
NB_MAX_MATERIALS = data["NB_MAX_MATERIALS"]

# Display similarity values and similarity threshold. outdated
GRAPH_COMPARISON = data["GRAPH_COMPARISON"]

# ========== DATA PROCESSING ===========
# parameters for data processing

SR = data["SR"]
HOP_LENGTH = data["HOP_LENGTH"]
if processing == 'symbols' or processing == 'vectors':
   SR = 1
   HOP_LENGTH = 1

PRECISION = data["PRECISION"]
NB_NOTES = data["NB_NOTES"]*PRECISION
NB_MFCC = data["NB_MFCC"]
INIT = data["INIT"]

MFCC_BIT = data["MFCC_BIT"]
CQT_BIT = data["CQT_BIT"]
FFT_BIT = data["FFT_BIT"]

if MFCC_BIT + CQT_BIT + FFT_BIT != 1:
   MFCC_BIT = 0
   CQT_BIT = 1
   FFT_BIT = 0

if processing == 'vectors':
   MFCC_BIT = 0
   CQT_BIT = 0
   FFT_BIT = 0

if CQT_BIT:
   NB_VALUES = NB_NOTES
elif MFCC_BIT:
   NB_VALUES = NB_MFCC
else:
   NB_VALUES = 0

# cqt
NOTES_PER_OCTAVE = data["NOTES_PER_OCTAVE"]*PRECISION
NOTE_MIN = data["NOTE_MIN"]

# fft
# 0.5 for quarter_tone, 1 for
# half-tone, 2 for tone
FREQ_WINDOWS = data["FREQ_WINDOWS"]
FREQ_BANDS = data["FREQ_BANDS"]
FREQ_BASIC = data["FREQ_BASIC"]
if FREQ_WINDOWS + FREQ_BANDS + FREQ_BASIC != 1:
    FREQ_WINDOWS = 1
    FREQ_BANDS = 0
    FREQ_BASIC = 0

TONE_PRECISION = data["TONE_PRECISION"]
DIV = data["DIV"]

TIME_STATS = data["TIME_STATS"]

MFCC_NORMALISATION = data["MFCC_NORMALISATION"]
CLEAN_SPECTRUM = data["CLEAN_SPECTRUM"]

# ------------- MIDI ------------------
# parameters for obtention of formal
# diagram from MIDI file

TEMPO = data["TEMPO"]

# ------------ ALGOCOG ----------------
# At signal level only

# Boolean to chose to reclassify or not
# transitory frames
CORRECTION_BIT = data["CORRECTION_BIT"]
# Boolean to chose to print in different
# color or not transitory frames that
# are moves
CORRECTION_BIT_COLOR = data["CORRECTION_BIT_COLOR"]
# Boolean to chose to print in different
# color or not segmentation frames
SEGMENTATION_BIT = data["SEGMENTATION_BIT"]
# Boolean to chose to write some statistics
# in a text file
WRITE_RESULTS = data["WRITE_RESULTS"]

# Number of frames corresponding to silence
# that we want to add at the beggining of the
# audio file
if processing == "signal":
   NB_SILENCE = data["NB_SILENCE"]*data["HOP_LENGTH"]
else:
   NB_SILENCE = 0

# Type of algorithm we want to use. ALGO_REP
# and ALGO_USUAL ar outdated.
ALGO_VMO = data["ALGO_VMO"]
ALGO_REP = data["ALGO_REP"]
ALGO_USUAL = data["ALGO_USUAL"]

# ----------- OUTPUT -----------------
# parameters to save or to show in .bmp
# or from pyplot
TO_SAVE_BMP = data["TO_SAVE_BMP"]
TO_SHOW_BMP = data["TO_SHOW_BMP"]
TO_SAVE_PYP = data["TO_SAVE_PYP"]
TO_SHOW_PYP = data["TO_SHOW_PYP"]
TO_SAVE_FINAL = data["TO_SAVE_FINAL"]

# to show or not the oracles
PLOT_ORACLE = data["PLOT_ORACLE"]
# to show the evolution of the formal
# diagrams
EVOL_PRINT = data["EVOL_PRINT"]

#to show the mso content:
SHOW_MSO_CONTENT = data["SHOW_MSO_CONTENT"]

#to show the computed costs (work only if
# costs are computed)
SHOW_COMPUTE_COSTS = data["SHOW_COMPUTE_COSTS"]

#print the computing time
SHOW_TIME = data["SHOW_TIME"]

# Display comments
verbose = data["verbose"]

# Checkpoint
checkpoint = data["checkpoint"]

# Save materials as results
SAVE_MATERIALS = data["SAVE_MATERIALS"]
SAVE_PARAMETERS = data["SAVE_PARAMETERS"]

# ------------ DISPLAY ----------------
# Only for level 0
# For the upper levels, background is white
# by default and each objects color alternate
# between four different greys

# note : matrices are created in HSV
# H between 0 and 179
# S between 0 and 255
# V between 0 and 255

BASIC_FRAME = tuple(data["BASIC_FRAME"]) # black
BACKGROUND = tuple(data["BACKGROUND"])  # white
SEGMENTATION = tuple(data["SEGMENTATION"])  # red

# when CORRECTION BIT is activated and a
# frame is moved because of wrong segmentation
# (SEG_ERROR) or similarity (CLASS ERROR)
SEG_ERROR = tuple(data["SEG_ERROR"])  # light green
CLASS_ERROR = tuple(data["CLASS_ERROR"])  # dark green

SILENT_FRAME = BACKGROUND

# ------------ VMO ---------------
# Parameters that are specifics to the
# VMO

# activate for more flexibility in the
# choice of the materials
PARCOURS = data["PARCOURS"]
# If parcours is activate, choose how much
# frames can be modified backward
INCERTITUDE = data["INCERTITUDE"]

# Type of VMO we want to use. Ref to the
# VMO documentation for more information
SUFFIX_METHOD = data["SUFFIX_METHOD"] # 'inc' ou 'complete'

# If we want to resynthesis the obtained VMO
# at level 0.
SYNTHESIS = data["SYNTHESIS"]

# COSTS
# TODO: le calcul des coûts n'est pas encore finalisé.
COMPUTE_COSTS = data["COMPUTE_COSTS"]
# 0 for time related to state,
# 1 for time related to actual computing time,
# 2 for max time at every levels (pseudo cognitive time)

STATE_TIME = data["STATE_TIME"]
COMPUTING_TIME = data["COMPUTING_TIME"]
MAX_TIME = data["MAX_TIME"]

TIME_TYPE = MAX_TIME
if TIME_TYPE < 0 or TIME_TYPE > 2:
    TIME_TYPE = COMPUTING_TIME

# HYPOTHESIS
COMPUTE_HYPOTHESIS = data["COMPUTE_HYPOTHESIS"]

NSNC = data["NSNC"] # no similarity, no completion
NSC = data["NSC"] # no similarity, completion
SNC = data["SNC"] # similarity, no completion
SC = data["SC"] # similarity, completion

global ind_lvl0_prev
global ind_lvl0

global time_tab
global phases, bit_class, bit_seg
global hypo, hypo1, hypo2, hypo3, hypo4, hypo_time
global hypo1_cost, hypo2_cost, hypo3_cost, hypo4_cost
hypo_value = data["hypo_value"]
