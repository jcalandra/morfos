import numpy as np
import librosa
import tensorflow as tf
from tensorflow.keras import layers, models
from scipy.spatial.distance import euclidean

# -------------------------
# Paramètres
# -------------------------
sr = 16000
frame_duration = 1.0   # 1 seconde par trame
n_mels = 64
latent_dim = 64
change_threshold = 0.05  # seuil pour détecter un changement de segment

# -------------------------
# Auto-encodeur CNN simple
# -------------------------
input_shape = (n_mels, 64, 1)
encoder_input = layers.Input(shape=input_shape)
x = layers.Conv2D(32, (3,3), activation='relu', padding='same', strides=(2,2))(encoder_input)
x = layers.Conv2D(64, (3,3), activation='relu', padding='same', strides=(2,2))(x)
x = layers.Flatten()(x)
latent = layers.Dense(latent_dim, name='latent_vector')(x)
encoder = models.Model(encoder_input, latent)

# -------------------------
# Fonction mel-spectrogramme
# -------------------------
def extract_mel_spectrogram(audio, sr=16000, n_mels=64, n_fft=1024, hop_length=256):
    S = librosa.feature.melspectrogram(y=audio, sr=sr, n_mels=n_mels, n_fft=n_fft, hop_length=hop_length)
    log_S = librosa.power_to_db(S, ref=np.max)
    log_S = log_S / 80.0 + 1.0  # normalisation [0,1]
    if log_S.shape[1] < 64:
        log_S = np.pad(log_S, ((0,0),(0,64-log_S.shape[1])), mode='constant')
    else:
        log_S = log_S[:, :64]
    return log_S[..., np.newaxis]

# -------------------------
# Traitement audio
# -------------------------
audio, sr = librosa.load("ML/sonate-au-clair-de-lune-allegretto.wav", sr=sr)
frame_length = int(sr * frame_duration)
prev_embedding = None
segment_boundaries = [0]  # index des frames où un segment commence

for start in range(0, len(audio), frame_length):
    frame = audio[start:start+frame_length]
    if len(frame) < frame_length:
        frame = np.pad(frame, (0, frame_length-len(frame)), mode='constant')
    
    mel = extract_mel_spectrogram(frame)
    mel = np.expand_dims(mel, axis=0)
    
    latent_vec = encoder.predict(mel)[0]
    
    if prev_embedding is not None:
        dist = euclidean(prev_embedding, latent_vec)
        if dist > change_threshold:
            segment_boundaries.append(start)
            print(f"Changement détecté à {start/sr:.2f}s")
    
    prev_embedding = latent_vec

print("Segments détectés aux positions (samples) :", segment_boundaries)
