import librosa
import pydub
from matplotlib.pyplot import *
import math
import version1.parameters as prm

# In this file are implemented all functions that process the signal

SR = prm.SR
print("sr init", SR, prm.SR)
DIV = prm.DIV
TONE_PRECISION = prm.TONE_PRECISION
NPO = prm.NOTES_PER_OCTAVE
NOTE_MIN = prm.NOTE_MIN

MFCC_BIT = prm.MFCC_BIT
FFT_BIT = prm.FFT_BIT
CQT_BIT = prm.CQT_BIT

TIME_STATS = prm.TIME_STATS
MFCC_NORMALISATION = prm.MFCC_NORMALISATION
CLEAN_SPECTRUM = prm.CLEAN_SPECTRUM


# =============================================== DATA COMPUTING =======================================================
# TODO : dans la partie GET DATA, inclure le traitement des fichiers MIDI

# TODO : dans getdata() gérer les fichiers stéréo
# TODO : dans getdata() faire en sorte de passer les forrmat wav 16, 24 (et 32 déjà ok) bits
# TODO : dans get_frequency, enregistrer les spectres et et fréquences correspondantes enregistrées pour ne pas avoir à
#  les recalculer lorsque l'on modifie uniquement d'autres paramètres ultérieurs.
#  les recalculer lorsque l'on modifie uniquement d'autres paramètres ultérieurs.


# --------------- GET DATA : WAVEFORM (volume) AND SPECTRUM COMPUTING -------------------

def get_data(audio_path):
    """ Read the signal at path 'audio_path' and compute it's frame rate, the size
    of the signal, and it's duration"""
    if audio_path.split('.')[-1] == 'mp3':  # mp3 files are converted into wave files.
        mp3 = pydub.AudioSegment.from_mp3(audio_path)
        if prm.verbose:
            print("[INFO] Converting audio from mp3 to wav...")
        audio_path = audio_path.split('.')[-2] + ".wav"
        mp3.export(audio_path, format="wav")
    # rate, data = wave.read(audio_path)
    data, rate = librosa.load(audio_path, sr=SR)
    if type(data[0]) == np.ndarray:
        data = librosa.core.to_mono(data)  # we force the signal to be mono
    data_size = data.size
    data_length = data_size / rate
    if prm.verbose:
        print("[RESULT] frame rate = ", rate, ", data size =", data_size, ", duration =", data_length)
    return data, rate, data_size, data_length

# ------------------------- FROM FFT -----------------------------


# SPECTRUM

# basic
def get_frequency_basic(data, rate, f0, hop_length):
    """ get the amplitude for each frequency of the signal 'data'
    of frame rate 'rate' included in the window which begin at t0 and end at
    t0+size."""
    frame = data[f0: f0 + hop_length]
    div = DIV
    fft = np.fft.fft(frame, int(rate/div))
    j = int(20000/div)
    spectrum = (np.absolute(fft)[:j])
    freq = np.arange(0, j*div, div)
    return freq, spectrum


# band
def clean_spectrum_band(n, len_null, spectrum):
    """ Clean the spectrum by keeping the highest frequencies in pikes. Induce to have an harmonic sound."""
    if spectrum[n - 1] >= spectrum[n - 2]:
        spectrum[n - 2] = 0
    elif spectrum[n - 2] > spectrum[n - 1] and (spectrum[n] > spectrum[n - 1]):
        for k in range(len_null + 1):
            spectrum[n - k] = 0
        len_null = 1
    elif spectrum[n - 2] > spectrum[n - 1] >= spectrum[n]:
        len_null = len_null + 1
    return spectrum, len_null


def freq_band(freq_min, freq_max, hop, div, fft, len_null, spectrum, freq):
    """ Compute the sum for each frequency band."""
    freq_min = int(freq_min/div)
    freq_max = int(freq_max/div)
    i = freq_min
    while i < freq_max:
        val = 0
        for j in range(hop):
            val = val + np.absolute(fft)[i]
            i = i + 1
        val = val/hop
        spectrum = np.append(spectrum, val)
        freq = np.append(freq, (i - hop) * div)
        if i > 2:
            n = len(spectrum) - 1
            if CLEAN_SPECTRUM:
                spectrum, len_null = clean_spectrum_band(n, len_null, spectrum)
    return spectrum, freq, len_null


def get_frequency_bands(data, rate, f0, hop_length):
    """ get the amplitude for each frequency of the signal 'data'
    of frame rate 'rate' included in the window which begin at t0 and end at
    t0+size."""
    frame = data[f0: f0 + hop_length]
    div = DIV
    fft = np.fft.fft(frame, int(rate/div))
    j = int(140/div)
    spectrum = (np.absolute(fft)[:j])
    freq = np.arange(0, j*div, div)

    len_null = 1
    if CLEAN_SPECTRUM:
        for n in range(2, j):
            spectrum, len_null = clean_spectrum_band(n, len_null, spectrum)
    spectrum, freq, len_null = freq_band(140, 360, 1, div, fft, len_null, spectrum, freq)
    spectrum, freq, len_null = freq_band(360, 700, 2, div, fft, len_null, spectrum, freq)
    spectrum, freq, len_null = freq_band(700, 1760, 5, div, fft, len_null, spectrum, freq)
    spectrum, freq, len_null = freq_band(1760, 4000, 10, div, fft, len_null, spectrum, freq)
    spectrum, freq, len_null = freq_band(4000, 8000, 25, div, fft, len_null, spectrum, freq)
    spectrum, freq, len_null = freq_band(8000, 17000, 50, div, fft, len_null, spectrum, freq)
    spectrum, freq, len_null = freq_band(17000, 20000, 125, div, fft, len_null, spectrum, freq)

    return freq, spectrum


# multi-windows
def clean_spectrum(spectrum):
    """ Clean the spectrum by keeping the highest frequencies in pikes. Induce to have an harmonic sound."""
    len_null = 1
    for i in range(2, len(spectrum)):
        if spectrum[i - 1] >= spectrum[i - 2]:
            spectrum[i - 2] = 0
        elif spectrum[i - 2] > spectrum[i - 1] and (spectrum[i] > spectrum[i - 1]):
            for k in range(1, len_null + 1):
                spectrum[i - k] = 0
            len_null = 1
        elif spectrum[i - 2] > spectrum[i - 1] >= spectrum[i]:
            len_null = len_null + 1
    return spectrum


def get_frequency_windows(data, rate, f0, hop_length):
    """ get the amplitude for each frequency of the signal 'data'
    of frame rate 'rate' included in the window which begin at t0 and end at
    t0+size."""
    frame = data[f0: f0 + hop_length]
    tab_freq = [34, 73, 130, 261, 554, 1102, 2216, 4434, 8869, 17739, 20000]
    div = TONE_PRECISION
    prec_j = prec_ind = 0
    spectrum = freq = []
    for i in range(len(tab_freq)):
        fft = np.fft.fft(frame, int(rate/div))
        j = int(tab_freq[i]/div)
        spectrum = np.append(spectrum, np.absolute(fft)[prec_j:j])
        freq = np.append(freq, np.arange(prec_ind, j*div, div))
        prec_ind = j*div
        div = div*2
        prec_j = int(tab_freq[i]/div)
    # graph_frequency(freq, spectrum)
    return freq, spectrum


def get_n_frequencies(data, rate, hop_length, nb_hop, init):
    """ Get the frequency spectrum for each windows of duration 'frame_length' in the data """
    f = init
    s_tab = []
    if prm.FREQ_WINDOWS:
        for i in range(nb_hop):
            s_tab.append(get_frequency_windows(data, rate, f, hop_length)[1])
            f = f + hop_length
    elif prm.FREQ_BANDS:
        for i in range(nb_hop):
            s_tab.append(get_frequency_bands(data, rate, f, hop_length)[1])
            f = f + hop_length
    elif prm.FREQ_BASIC:
        for i in range(nb_hop):
            s_tab.append(get_frequency_basic(data, rate, f, hop_length)[1])
            f = f + hop_length
    else:
        for i in range(nb_hop):
            s_tab.append(get_frequency_basic(data, rate, f, hop_length)[1])
            f = f + hop_length
    return s_tab


# VOLUME
def get_n_volumes(data, hop_length, nb_hop, init):
    """ Cut the tab data into batches of size hop_length.
    These batches corresponds to the frames."""
    n = nb_hop
    vn_tab = [[] for i in range(n)]
    for i in range(n - 1):
        for j in range(hop_length):
            vn_tab[i].append(data[i*hop_length + j + init])
    for j in range(len(data) - init - (n - 1) * hop_length):
        vn_tab[n - 1].append(data[(n - 1) * hop_length + j + init])
    return vn_tab


def get_max_volumes(data, hop_length, nb_hop, init):
    """ Return the max volume for each frame of data."""
    vn_tab = get_n_volumes(data, hop_length, nb_hop, init)
    v_tab = []
    for i in range(len(vn_tab)):
        val = max(vn_tab[i])
        if val == 0:
            v_tab.append(val)
        else:
            v_tab.append(math.log(val))
    return v_tab


def get_rms_volumes(data, hop_length, nb_hop, init):
    """ Compute the root mean square of every volumes for each frame of data."""
    vn_tab = get_n_volumes(data, hop_length, nb_hop, init)
    v_tab = []
    mean_vtab = 0
    for i in range(len(vn_tab)):
        v_tab_i = 0
        n = len(vn_tab[i])
        for j in range(n):
            v_tab_i = v_tab_i + (vn_tab[i][j])**2
        if n != 0:
            v_tab_i = math.sqrt(v_tab_i/n)
        v_tab.append(v_tab_i)
        mean_vtab = mean_vtab + v_tab_i

    # Volumes are normalised between 0 and 1
    n = len(v_tab)
    min_rms = min(v_tab)
    max_rms = max(v_tab) - min_rms
    for i in range(n):
        if v_tab[i] == 0:
            v_tab[i] = 0
        else:
            v_tab[i] = (v_tab[i] - min_rms)/max_rms
    return v_tab


def get_fft_descriptors(data, rate, hop_length, nb_hop, init):
    """ returns frequency and volume descriptors computed with fft."""
    start_time_vol = time.time()
    v_tab = get_rms_volumes(data, hop_length, nb_hop, init)
    vol_time = time.time() - start_time_vol
    if prm.SHOW_TIME:
        print("Temps de calcul v_tab : %s secondes ---" % vol_time)

    start_time_freq = time.time()
    s_tab = get_n_frequencies(data, rate, hop_length, nb_hop, init)

    spec_time = time.time() - start_time_freq
    full_time = vol_time + spec_time
    if prm.SHOW_TIME:
        print("Temps de calcul s_tab : %s secondes ---" % spec_time)
        print("Temps de calcul total : %s secondes ---" % full_time)

    if TIME_STATS:
        f_s = open("../../results/fft_spectrum.txt", "a")
        f_v = open("../../results/fft_volume.txt", "a")
        f_full = open("../../results/fft_full.txt", "a")
        f_s.write(str(spec_time) + "\n")
        f_s.close()
        f_v.write(str(vol_time) + "\n")
        f_v.close()
        f_full.write(str(full_time) + "\n")
        f_full.close()

    return v_tab, s_tab


# -------------------------- FROM MFCC ---------------------------

def mel_fcc(data, rate, hop_length, nb_mfcc):
    """ compute the mel frequency sceptral coefficients of the audio at audio_path,every 'hop_length' frames"""
    mfcc_tab = librosa.feature.mfcc(y=data, sr=rate, hop_length=hop_length, n_mfcc=nb_mfcc)
    return mfcc_tab


def get_mfcc_descriptors(data, rate, hop_length, nb_mfcc, init):
    """ returns frequency and volume descriptors computed with mfcc."""
    start_time = time.time()
    mfcc_tab = mel_fcc(data[init:], rate, hop_length, nb_mfcc)
    start_time_vol = time.time()
    v_tab = 1 - abs(mfcc_tab[0]/max(abs(mfcc_tab[0])))
    vol_time = time.time() - start_time

    start_time_freq = time.time()

    # Normalisation of the mfccs
    if MFCC_NORMALISATION:
        mean = np.mean(mfcc_tab)
        sd = np.std(mfcc_tab)
        n_mfcc_tab = mfcc_tab
        n_mfcc_tab = np.subtract(n_mfcc_tab, mean)
        n_mfcc_tab = n_mfcc_tab/sd
    s_tab = mfcc_tab[1:]
    if MFCC_NORMALISATION:
        for i in range(len(s_tab)):
            mean_s_tab_i = np.mean(s_tab[i])
            standard_deviation = np.std(s_tab[i])
            n = len(s_tab[i])
            for j in range(n):
                s_tab[i][j] = s_tab[i][j] - mean_s_tab_i
            s_tab[i] = s_tab[i] / standard_deviation

    if TIME_STATS:
        if prm.SHOW_TIME:
            print("Temps de calcul v_tab : %s secondes ---" % vol_time)
        spec_time = (time.time() - start_time_freq) + (start_time_vol - start_time)
        full_time = time.time() - start_time
        if prm.SHOW_TIME:
            print("Temps de calcul s_tab : %s secondes ---" % spec_time)
            print("Temps de calcul total : %s secondes ---" % full_time)
        f_s = open("../../results/mfcc_spectrum.txt", "a")
        f_v = open("../../results/mfcc_volume.txt", "a")
        f_full = open("../../results/mfcc_full.txt", "a")
        f_s.write(str(spec_time) + "\n")
        f_s.close()
        f_v.write(str(vol_time) + "\n")
        f_v.close()
        f_full.write(str(full_time) + "\n")
        f_full.close()
    return v_tab, s_tab

# -------------------------- FROM CQT ---------------------------


def get_cqt(data, rate, hop_length, nb_notes, init, fmin):
    """ Get the cqt from the audio 'data'."""
    cqt_values = np.abs(librosa.cqt(data[init:], sr=rate, hop_length=hop_length, fmin=librosa.note_to_hz(fmin),
                           n_bins=nb_notes, bins_per_octave=NPO, window='blackmanharris', sparsity=0.01, norm=1))
    cqt_values = librosa.amplitude_to_db(cqt_values, ref=np.max)
    return cqt_values


def get_cqt_descriptors(data, rate, hop_length, nb_hop, nb_values, init, fmin):
    """ returns frequency and volume descriptors computed with cqt."""
    start_time_vol = time.time()
    v_tab = get_rms_volumes(data, hop_length, nb_hop, init)
    vol_time = time.time() - start_time_vol

    start_time_freq = time.time()
    s_tab = get_cqt(data, rate, hop_length, nb_values, init, fmin)

    if TIME_STATS:
        spec_time = time.time() - start_time_freq
        if prm.SHOW_TIME:
            print("Temps de calcul v_tab : %s secondes ---" % vol_time)
        full_time = vol_time + spec_time
        if prm.SHOW_TIME:
            print("Temps de calcul s_tab : %s secondes ---" % spec_time)
            print("Temps de calcul total : %s secondes ---" % full_time)
        f_s = open("../../results/cqt_spectrum.txt", "a")
        f_v = open("../../results/cqt_volume.txt", "a")
        f_full = open("../../results/cqt_full.txt", "a")
        f_s.write(str(spec_time) + "\n")
        f_s.close()
        f_v.write(str(vol_time) + "\n")
        f_v.close()
        f_full.write(str(full_time) + "\n")
        f_full.close()
    return v_tab, s_tab


# ------------------------ FROM SPECTRAL CENTROID ----------------

def get_central_spectroid(data, rate, hop_length, nb_notes, init, fmin):
    cspect = librosa.feature.spectral_centroid(data[init:], sr=rate, S=None, n_fft=2048, hop_length=hop_length,
                                      freq=None, win_length=None, window='hann', center=True, pad_mode='constant')
    return cspect

def get_central_spectroid_descriptors(data, rate, hop_length, nb_hop, nb_values, init, fmin):
    v_tab = get_rms_volumes(data, hop_length, nb_hop, init)
    s_tab = get_cqt(data, rate, hop_length, nb_values, init, fmin)
    return v_tab, s_tab



# ------------------------- FACTORISATION ------------------------


def get_descriptors(data, rate, hop_length, nb_hop, nb_values, init, fmin='C1'):
    """ returns frequency and volume descriptors computed with any kind of descriptors depending on the parameters."""
    v_tab = s_tab = 0
    if MFCC_BIT:
        v_tab, s_tab = get_mfcc_descriptors(data, rate, hop_length, nb_values, init)
    elif FFT_BIT:
        v_tab, s_tab = get_fft_descriptors(data, rate, hop_length, nb_hop, init)
    elif CQT_BIT:
        v_tab, s_tab = get_cqt_descriptors(data, rate, hop_length, nb_hop, nb_values, init, fmin)
    return v_tab, s_tab


# -------------------- GET DATA : MIDI FILES ----------------------


# ------------------------ PRINT EVERYTHING -----------------------

def graph_amplitude(data, rate, n, x_max):
    """ Draw the graphic of the amplitude of the signal represented by
    the table 'data' through time of sizce n and frame rate 'rate'. Draw
     the graph from time 0 to x_max seconds."""
    t = np.arange(n) / rate
    figure(figsize=(12, 4))
    plot(t, data)
    xlabel("t (s)")
    ylabel("amplitude")
    axis([0, x_max, data.min(), data.max()])
    show()


def graph_frequency(freq, spectrum):  # frame0, frame_size
    """ Draw the graphic of amplitude for each frequency of the signal 'data'
    of frame rate 'rate' included in the window which begin at t0 and end at
    t0+size."""
    figure(figsize=(12, 4))
    vlines(freq, [0], spectrum, 'r')
    xlabel('f (Hz)')
    ylabel('A')
    axis(xlim=(0, freq), ylim=(0, spectrum.max()))
    show()
    return freq, spectrum
