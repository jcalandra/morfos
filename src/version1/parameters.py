# ================================================= PARAMETERS =========================================================
# This is the parametrisation file of the system
# Any variable tha can be modified by the users of the system are here.
# In the interface, numbers might be changed by virtual potentiometers, colors...

import sys
from pathlib import Path # if you haven't already done so
file = Path(__file__).resolve()
project_root = str(file.parents[1])

import json
with open(project_root + '/version1/parameters.json') as json_parameters:
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
POLYPHONY = data["POLYPHONY"]

# A value that determine the color variation if pseudo-polyphony is displayed
min_matrix = data["min_matrix"]
if min_matrix >= 1:
   min_matrix = 0.999
elif min_matrix < 0:
   min_matrix = 0

# Choose here either to process the cognitive algorithm from signal or character string
# processing must be str 'symbols' or 'signal' or 'vectors'
processing = data["processing"]
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

RULE_1a = data["RULE_1a"]
RULE_1b = data["RULE_1b"]
RULE_2 = data["RULE_2"]
RULE_3 = data["RULE_3"]
RULE_4 = data["RULE_4"]
RULE_5a = data["RULE_5a"]
RULE_5b = data["RULE_5b"]
RULE_6 = data["RULE_6"]
RULE_7 = data["RULE_7"]
RULE_8 = data["RULE_8"]

ALIGNEMENT_rule3 = data["ALIGNEMENT_rule3"]
ALIGNEMENT_rule4 = data["ALIGNEMENT_rule4"]
lower_bound_rule6 = data["lower_bound_rule6"]
higher_bound_rule6 = data["higher_bound_rule6"]

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
NB_SILENCE = data["NB_SILENCE"]*1024

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
SAVE_MATERIALS = 1

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
global time_tab

global lambda_0, gamma, alpha, delta, beta, start_time_t, real_time_t, max_time_t
global lambda_levels, gamma_levels, alpha_levels, delta_levels, beta_levels # per levels
global lambda_sum, gamma_sum, alpha_sum, delta_sum, beta_sum # sum per level
global lambda_tab, gamma_tab, alpha_tab, delta_tab, beta_tab # total sum
global lambda_time, gamma_time, alpha_time, delta_time, beta_time

global cost_0_init, \
   cost_1_nb_comparison, \
   cost_2_ext_forward_link, \
   cost_3_sfx_candidate, \
   cost_3b_complete, \
   cost_4_nb_comparison_rep, \
   cost_5_sfx_candidate_rep, \
   cost_6_nb_comparison_parcours, \
   cost_7_sfx_candidate_parcours, \
   cost_8_sfx, \
   cost_9_new_mat, \
   cost_10_update_mat, \
   cost_11_nb_comparison_update, \
   cost_12_cost_sfx_update, \
   cost_13_last_update

global cost_14_find_sfx, \
   cost_15_rep, \
   cost_16_parcours, \
   cost_17_fix_sfx, \
   cost_18_update

global cost_19_comparisons, \
   cost_20_sfx_candidates, \
   cost_21_statics

global cost_22_theoretical, \
   cost_23_theoretical_and_mat

global cost_24_total_wo_correct, \
   cost_25_total_wo_correct_w_update, \
   cost_total

global cost_0_init_tab, \
   cost_1_nb_comparison_tab, \
   cost_2_ext_forward_link_tab, \
   cost_3_sfx_candidate_tab, \
   cost_3b_complete_tab, \
   cost_4_nb_comparison_rep_tab, \
   cost_5_sfx_candidate_rep_tab, \
   cost_6_nb_comparison_parcours_tab, \
   cost_7_sfx_candidate_parcours_tab, \
   cost_8_sfx_tab, \
   cost_9_new_mat_tab, \
   cost_10_update_mat_tab, \
   cost_11_nb_comparison_update_tab, \
   cost_12_cost_sfx_update_tab, \
   cost_13_last_update_tab

global cost_14_find_sfx_tab, \
   cost_15_rep_tab, \
   cost_16_parcours_tab, \
   cost_17_fix_sfx_tab, \
   cost_18_update_tab

global cost_19_comparisons_tab, \
   cost_20_sfx_candidates_tab, \
   cost_21_statics_tab

global cost_22_theoretical_tab, \
   cost_23_theoretical_and_mat_tab

global cost_24_total_wo_correct_tab, \
   cost_25_total_wo_correct_w_update_tab, \
   cost_total_tab, \
   cost_total_sum, \
   cost_time

cost_new_oracle = data["cost_new_oracle"]
cost_numerisation = data["cost_numerisation"]
cost_desc_computation = data["cost_desc_computation"]
cost_oracle_acq_signal = data["cost_oracle_acq_signal"]
cost_seg_test_1 = data["cost_seg_test_1"]
cost_new_mat_creation = data["cost_new_mat_creation"]
cost_maj_autosim = data["cost_maj_autosim"]
cost_maj_historique = data["cost_maj_historique"]
cost_maj_df = data["cost_maj_df"]
cost_print_df = data["cost_print_df"]
cost_polyphonie = data["cost_polyphonie"]
cost_oracle_acq_symb = data["cost_oracle_acq_symb"]
cost_seg_test_2 = data["cost_seg_test_2"]
cost_maj_concat_obj = data["cost_maj_concat_obj"]
cost_test_EOS = data["cost_test_EOS"]
cost_comparaison_2 = data["cost_comparaison_2"]
cost_labelisation = data["cost_labelisation"]
cost_maj_link = data["cost_maj_link"]
cost_level_up = data["cost_level_up"]

# HYPOTHESIS
COMPUTE_HYPOTHESIS = data["COMPUTE_HYPOTHESIS"]

NSNC = data["NSNC"] # no similarity, no completion
NSC = data["NSC"] # no similarity, completion
SNC = data["SNC"] # similarity, no completion
SC = data["SC"] # similarity, completion

global hypo, hypo1, hypo2, hypo3, hypo4, hypo_time
global hypo1_cost, hypo2_cost, hypo3_cost, hypo4_cost
hypo_value = data["hypo_value"]
