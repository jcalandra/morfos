import numpy as np
import oracle
import oracle_ac
import generate as vge
import matplotlib.pyplot as plt
import time
import sklearn.preprocessing as pre
import librosa
import scipy.io.wavfile as wave
import plot

# LOAD AUDIO FILE
target_file = '../../../../data/songs/mus_med/Carmen/sequence_1_midi_piano.wav'
playback_y, sr1 = librosa.load(target_file)

# IPython.display.Audio(data=playback_y, rate=sr)

# PARAMETERS
sample_rate = 22050
fft_size = 2048
hop_size = 1024

# ANALYSIS
# chroma
'''
y, sr = librosa.load(target_file, sr=sample_rate)
C = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=fft_size, hop_length=hop_size, octwidth=None)
feature = np.log(C+np.finfo(float).eps)
feature = pre.normalize(feature)

chroma_frames = feature.transpose()
r = (0.00, 1.01, 0.01)
ideal_t = oracle.find_threshold(chroma_frames, r=r, flag='a', dim=12)
print(ideal_t[0][1])
oracle_t = oracle.build_oracle(chroma_frames, flag='a', threshold=ideal_t[0][1], feature='chroma', dim=12)
print(oracle_t.data)
'''
# cqt
start_time_full = time.time()
NB_NPO = 12
PRECISION = 4
NB_OCTAVES = 4
DIM = NB_OCTAVES*NB_NPO*PRECISION

here_time = time.time()
datanum, sr = librosa.load(target_file, sr=sample_rate)
temps_data = time.time() - here_time
print("Temps data : %s secondes ---" % temps_data)

cqt_values = np.abs(librosa.cqt(datanum, sr=sr, hop_length=hop_size, fmin=librosa.note_to_hz('C3'),
                    n_bins=DIM, bins_per_octave=NB_NPO*PRECISION, window='blackmanharris', sparsity=0.01, norm=1))
feature = librosa.amplitude_to_db(cqt_values, ref=np.max)
# feature = pre.normalize(feature)

cqt_frames = feature.transpose()
print("cqt frames :", cqt_frames)
r = (0.00, 1.01, 0.01)
# ideal_t = oracle.find_threshold(cqt_frames, r=r, flag='a', dim=DIM)
oracle_t = oracle.build_oracle(cqt_frames, flag='a', threshold=0.028, dfunc='cosine', suffix_method='inc', dim=DIM)

print("Temps d execution de l'algorithme entier : %s secondes ---" % (time.time() - start_time_full))


# mfcc
'''y, sr = librosa.load(target_file, sr=sample_rate)
C = librosa.feature.mfcc(y=y, sr=sr, S=None, n_mfcc=20, hop_length=hop_size)
feature = librosa.core.power_to_db(C)
feature = pre.normalize(feature)

mfcc_frames = feature.transpose()
r = (0.0, 1.01, 0.01)
ideal_t = oracle.find_threshold(mfcc_frames, r = r,flag = 'a', dim=20)
oracle_t = oracle.build_oracle(mfcc_frames, flag = 'a', threshold = ideal_t[0][1], feature = 'mfcc', dim=20)
'''

# PLOT
'''
x = np.array([i[1] for i in ideal_t[1]])
y = [i[0] for i in ideal_t[1]]
fig = plt.figure(figsize=(10, 3))
plt.plot(x, y, linewidth=2)
plt.title('IR vs. Threshold Value(vmo)', fontsize=18)
plt.grid(b='on')
plt.xlabel('Threshold', fontsize=14)
plt.ylabel('IR', fontsize=14)
plt.xlim(0, 0.2)
plt.tight_layout()
plt.show()
plt.close()
'''

# FORMAL DIAGRAM

max_mat = max(oracle_t.data[1:]) + 1
nb_hop = len(oracle_t.data)
color = 0

mtx = np.ones((max_mat, nb_hop), np.uint8)
mtx[0][0] = color

for i_hop in range(1, nb_hop):  # while
    j_mat = oracle_t.data[i_hop]
    mtx[j_mat][i_hop] = color
print(oracle_t.data)
print(oracle_t.sfx)
print(oracle_t.trn)
print(oracle_t.lrs)
print(oracle_t.max_lrs)
plt.figure(figsize=(32, 20))
plt.gray()
plt.title('Geisslerlied')
plt.xlabel("temps (mémoire forme)")
plt.ylabel("matériau (mémoire matériau)")
plt.imshow(mtx, extent=[0, nb_hop*(hop_size/sample_rate), max_mat, 0])
plt.show()
plt.close()


# IMPRO SYNTHESIS
'''seq = vge.improvise(oracle_t, seq_len=oracle_t.n_states-1, LRS=2, weight='lrs')
x, _w, new_sr = vge.audio_synthesis(target_file, 'vmo_synthesis_test.wav', seq,
                                    analysis_sr=sample_rate, buffer_size=fft_size, hop=hop_size)'''
'''
# RESYNTHESIS
new_y = np.array([])
for i in range(1, nb_hop):
    latent = oracle_t.latent[int(oracle_t.data[i])]
    sound = datanum[latent[3]*hop_size:(latent[3] + 1)*hop_size]
    new_y = np.concatenate((new_y, sound))

wave.write('synthesis.wav', sr, new_y)'''

# PLOT THE ORACLE
im = plot.start_draw(oracle_t, size=(900 * 4, 400 * 4))
im.show()
